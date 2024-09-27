from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime

from .stats import ExecutionStats

class OutputStateStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"
    CANCELLED = "cancelled"

class OutputState(BaseModel):
    status: OutputStateStatus
    value: Any

class NodeExecutionStatus(str, Enum):
    PENDING = "pending"
    RETRY = "retry"
    STARTING = "starting"
    RUNNING = "running"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    ERROR = "error"

class NodeExecutionState(BaseModel):
    status: NodeExecutionStatus
    inputs: Optional[Dict[str, Any]] = None
    outputs: Optional[Dict[str, OutputState | None]] = None
    updatedAt: datetime
    errors: Optional[List[Any]] = None
    message: Optional[str] = None
    retries: int
    stats: Optional[ExecutionStats] = None

    @staticmethod
    def is_waiting(state: 'NodeExecutionState') -> bool:
        return state.status == NodeExecutionStatus.PENDING

    @staticmethod
    def is_starting(state: 'NodeExecutionState') -> bool:
        return state.status in {NodeExecutionStatus.STARTING, NodeExecutionStatus.RETRY}

    @staticmethod
    def is_started(state: 'NodeExecutionState') -> bool:
        return state.status == NodeExecutionStatus.RUNNING

    @staticmethod
    def is_ended(state: 'NodeExecutionState') -> bool:
        return state.status in {NodeExecutionStatus.FINISHED, NodeExecutionStatus.ERROR, NodeExecutionStatus.CANCELLED}

    @staticmethod
    def is_failed(state: 'NodeExecutionState') -> bool:
        return state.status in {NodeExecutionStatus.ERROR, NodeExecutionStatus.CANCELLED}

    @staticmethod
    def is_succeeded(state: 'NodeExecutionState') -> bool:
        return state.status == NodeExecutionStatus.FINISHED