from pydantic import BaseModel, RootModel, Field
from typing import Any, Dict, List, Optional, Union, Literal, Callable
from enum import Enum
from datetime import datetime

from .agent import Agent
from .node_execution import (
    NodeExecutionState,
    NodeExecutionStatus,
    OutputStateStatus,
)
from .stats import ExecutionStats

class AgentExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    FINISHED = "finished"
    ERROR = "error"

class BaseEvent(BaseModel):
    createdAt: datetime

class ExecutionEventOp(str, Enum):
    INIT = "init"
    UPDATE_STATUS = "updateStatus"
    OUTPUT_UPDATE = "output.update"
    NODE_UPDATE_STATUS = "node.updateStatus"
    NODE_OUTPUT_UPDATE_STATUS = "node.output.updateStatus"
    NODE_OUTPUT_UPDATE = "node.output.update"

class InitEvent(BaseEvent):
    op: Literal[ExecutionEventOp.INIT]
    execution: 'AgentExecution'

class UpdateStatusEvent(BaseEvent):
    op: Literal[ExecutionEventOp.UPDATE_STATUS]
    status: AgentExecutionStatus
    message: Optional[str] = None
    errors: Optional[List[Any]] = Field(alias="_errors", default=None)

class OutputUpdateEvent(BaseEvent):
    op: Literal[ExecutionEventOp.OUTPUT_UPDATE]
    output: str
    value: Any
    append: Optional[bool] = None

class NodeUpdateStatusEvent(BaseEvent):
    op: Literal[ExecutionEventOp.NODE_UPDATE_STATUS]
    nodeId: str
    status: NodeExecutionStatus
    message: Optional[str] = None
    errors: Optional[List[Any]] = None
    stats: Optional[ExecutionStats] = None
    retries: Optional[int] = None

class NodeOutputUpdateStatusEvent(BaseEvent):
    op: Literal[ExecutionEventOp.NODE_OUTPUT_UPDATE_STATUS]
    nodeId: str
    output: str
    status: OutputStateStatus

class NodeOutputUpdateEvent(BaseEvent):
    op: Literal[ExecutionEventOp.NODE_OUTPUT_UPDATE]
    nodeId: str
    output: str
    status: OutputStateStatus
    value: Any
    append: Optional[bool] = None

class ExecutionEvent(RootModel):
    root: Union[
        InitEvent,
        UpdateStatusEvent,
        OutputUpdateEvent,
        NodeUpdateStatusEvent,
        NodeOutputUpdateStatusEvent,
        NodeOutputUpdateEvent,
    ] = Field(discriminator="op")

class AgentExecution(BaseModel):
    id: str = Field(alias="_id")
    status: AgentExecutionStatus
    updatedAt: datetime
    queuedAt: Optional[datetime] = None
    startedAt: Optional[datetime] = None
    finishedAt: Optional[datetime] = None
    pipelineId: Optional[str] = None
    pipeline: Agent
    externalId: Optional[str] = None
    state: Dict[str, NodeExecutionState]
    stats: Optional[ExecutionStats] = None
    inputs: Dict[str, Any]
    outputs: Optional[Dict[str, Any]] = None
    events: Optional[List[Union[InitEvent, UpdateStatusEvent, OutputUpdateEvent, NodeUpdateStatusEvent, NodeOutputUpdateStatusEvent, NodeOutputUpdateEvent]]] = None
    message: Optional[str] = None
    errors: Optional[List[Any]] = Field(alias="_errors", default=None)
    parentExecutionId: Optional[str] = None

    @staticmethod
    def is_ended(execution: 'AgentExecution') -> bool:
        return execution.status in {AgentExecutionStatus.FINISHED, AgentExecutionStatus.ERROR}

    @staticmethod
    def update(execution: 'AgentExecution', f: Callable[['AgentExecution'], 'AgentExecution'], get_timestamp=lambda: datetime.now()) -> 'AgentExecution':
        execution = f(execution)
        stats = {}
        for node_id, node_state in execution.state.items():
            node_stats = {}
            if node_state.stats:
                node_stats = node_state.stats.model_dump(by_alias=True)
            for stats_key, value in node_stats.items():
                stats[stats_key] = (stats.get(stats_key) or 0) + (value or 0)
        return execution.model_copy(
            update={
                "stats": ExecutionStats(**stats),
                "startedAt": execution.startedAt or datetime.now(),
                "updatedAt": get_timestamp(),
                "finishedAt": get_timestamp() if AgentExecution.is_ended(execution) and execution.finishedAt is None else execution.finishedAt,
            }
        )

    @staticmethod
    def update_agent_output(execution: 'AgentExecution', output_name: str, f, get_timestamp=lambda: datetime.now()) -> 'AgentExecution':
        return AgentExecution.update(
            execution,
            lambda e: e.copy(update={"outputs": {**e.outputs, output_name: f(e.outputs.get(output_name))}}),
            get_timestamp,
        )

    @staticmethod
    def update_node(execution: 'AgentExecution', node_id: str, f, get_timestamp=lambda: datetime.now()) -> 'AgentExecution':
        return AgentExecution.update(
            execution,
            lambda e: e.copy(update={"state": {**e.state, node_id: f(e.state.get(node_id)).copy(update={"updatedAt": get_timestamp()})}}),
            get_timestamp,
        )

    @staticmethod
    def update_node_output(execution: 'AgentExecution', node_id: str, output_name: str, f, get_timestamp=lambda: datetime.now()) -> 'AgentExecution':
        return AgentExecution.update_node(
            execution,
            node_id,
            lambda node_state: node_state.copy(
                update={
                    "outputs": {**node_state.outputs, output_name: f(node_state.outputs.get(output_name))}
                }
            ),
            get_timestamp,
        )

    @staticmethod
    def init(event: InitEvent) -> 'AgentExecution':
        return event.execution

    @staticmethod
    def apply_events(execution: 'AgentExecution') -> 'AgentExecution':
        if execution.events is None:
            return execution
        events = sorted(execution.events, key=lambda e: e.createdAt)
        for event in events:
            execution = AgentExecution.apply_event(execution, event)
        execution = execution.model_copy(update={"events": []})
        return execution

    @staticmethod
    def apply_event(execution: 'AgentExecution', event: Union[InitEvent, UpdateStatusEvent, OutputUpdateEvent, NodeUpdateStatusEvent, NodeOutputUpdateStatusEvent, NodeOutputUpdateEvent]) -> 'AgentExecution':
        if isinstance(event, InitEvent):
            return AgentExecution.init(event)
        elif isinstance(event, UpdateStatusEvent):
            return AgentExecution.apply_agent_event(execution, event)
        elif isinstance(event, OutputUpdateEvent):
            return AgentExecution.apply_agent_output_event(execution, event)
        elif isinstance(event, NodeUpdateStatusEvent):
            return AgentExecution.apply_node_event(execution, event)
        elif isinstance(event, (NodeOutputUpdateStatusEvent, NodeOutputUpdateEvent)):
            return AgentExecution.apply_node_output_event(execution, event)

    @staticmethod
    def apply_agent_event(execution: 'AgentExecution', event: UpdateStatusEvent) -> 'AgentExecution':
        return AgentExecution.update(
            execution,
            lambda e: e.model_copy(
                update={
                    "status": event.status,
                    "message": event.message or e.message,
                    "_errors": event.errors or e.errors,
                }
            ),
            lambda: event.createdAt,
        )

    @staticmethod
    def apply_agent_output_event(execution: 'AgentExecution', event: OutputUpdateEvent) -> 'AgentExecution':
        return AgentExecution.update_agent_output(
            execution,
            event.output,
            lambda output_value: f"{output_value or ''}{event.value}" if event.append else event.value,
            lambda: event.createdAt,
        )

    @staticmethod
    def apply_node_event(execution: 'AgentExecution', event: NodeUpdateStatusEvent) -> 'AgentExecution':
        return AgentExecution.update_node(
            execution,
            event.nodeId,
            lambda node: node.copy(
                update={
                    "status": event.status,
                    "retries": event.retries or node.retries,
                    "message": event.message or node.message,
                    "errors": event.errors or node.errors,
                    "stats": event.stats or node.stats,
                }
            ),
            lambda: event.createdAt,
        )

    @staticmethod
    def apply_node_output_event(execution: 'AgentExecution', event: Union[NodeOutputUpdateStatusEvent, NodeOutputUpdateEvent]) -> 'AgentExecution':
        return AgentExecution.update_node_output(
            execution,
            event.nodeId,
            event.output,
            lambda output_state: output_state.copy(
                update={
                    "status": event.status,
                    "value": f"{output_state.value or ''}{event.value}" if isinstance(event, NodeOutputUpdateEvent) and event.append else event.value,
                }
            ) if output_state else None,
            lambda: event.createdAt,
        )
