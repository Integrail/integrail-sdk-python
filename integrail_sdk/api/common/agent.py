import json

from pydantic import BaseModel
from typing import Any, Dict, Optional, Union, Callable, Coroutine
import aiohttp

from integrail_sdk.types import (
    AgentCategory,
    AgentExecution,
    AgentExecutionStatus,
    AgentSubcategory,
    ExecutionEvent,
    InitEvent,
    InlineAgent,
    NodeDefinition,
    UpdateStatusEvent,
)
from integrail_sdk.api.base import BaseApi, BaseResponse
from integrail_sdk.helpers.jsonl import jsonl


class BaseAgentApi(BaseApi):
    async def wrap_execution(
            self,
            url: str,
            payload: Dict[str, Any],
            on_event: Optional[Callable[[ExecutionEvent, Optional[AgentExecution]], Any]] = None,
            on_finish: Optional[Callable[[Optional[AgentExecution]], Coroutine[Any, Any, Any]]] = None,
    ) -> Union[None, 'AgentExecuteNonStreamingResponse']:
        if payload.get("stream") and on_event:
            async def handle_event(data):
                nonlocal execution
                event = ExecutionEvent(**data)
                if isinstance(event.root, InitEvent):
                    execution = AgentExecution(**event.root.execution.model_dump(by_alias=True))
                elif execution is not None:
                    events = []
                    if execution.events:
                        events = [*execution.events]
                    events.append(event.root)
                    execution_dict = execution.model_dump(by_alias=True)
                    execution_dict["events"] = events
                    execution = AgentExecution.apply_events(
                        AgentExecution(**execution_dict)
                    )
                else:
                    raise ValueError("Execution is None")
                if on_event:
                    await on_event(event, execution)
                if on_finish and isinstance(event.root, UpdateStatusEvent) and execution.status in [
                    AgentExecutionStatus.FINISHED, AgentExecutionStatus.CANCELLED, AgentExecutionStatus.ERROR]:
                    await on_finish(execution)

            async with aiohttp.ClientSession() as session:
                async with session.post(f'{self.options.baseUri}{url}', json=payload, headers={
                    'Authorization': f'Bearer {self.options.apiToken}',
                }) as response:
                    execution: Optional[AgentExecution] = None
                    await jsonl(response, handle_event)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'{self.options.baseUri}{url}', json=payload) as response:
                    return await response.json()

    async def wrap_execution_multipart(
            self,
            url: str,
            payload: Dict[str, Any],
            files: Dict[str, Any],
            on_event: Optional[Callable[[ExecutionEvent, Optional[AgentExecution]], Coroutine[Any, Any, Any]]] = None,
            on_finish: Optional[Callable[[Optional[AgentExecution]], Coroutine[Any, Any, Any]]] = None,
    ) -> Union[aiohttp.ClientResponse, 'AgentExecuteNonStreamingResponse']:
        form_data = aiohttp.FormData()
        for key, value in files.items():
            form_data.add_field(key, value)
        form_data.add_field("payload", json.dumps(payload))

        if payload.get("stream") and on_event:
            async def handle_event(data):
                nonlocal execution
                event = ExecutionEvent(**data)
                if isinstance(event.root, InitEvent):
                    execution = AgentExecution(**event.root.execution.model_dump(by_alias=True))
                elif execution is not None:
                    events = []
                    if execution.events:
                        events = [*execution.events]
                    events.append(event.root)
                    execution_dict = execution.model_dump(by_alias=True)
                    execution_dict["events"] = events
                    execution = AgentExecution.apply_events(
                        AgentExecution(**execution_dict)
                    )
                else:
                    raise ValueError("Execution is None")
                if on_event:
                    await on_event(event, execution)
                if on_finish and isinstance(event.root, UpdateStatusEvent) and execution.status in [
                    AgentExecutionStatus.FINISHED, AgentExecutionStatus.CANCELLED, AgentExecutionStatus.ERROR]:
                    await on_finish(execution)

            async with aiohttp.ClientSession() as session:
                async with session.post(f'{self.options.baseUri}{url}', data=form_data, headers={
                    'Authorization': f'Bearer {self.options.apiToken}',
                }) as response:
                    execution: Optional[AgentExecution] = None
                    await jsonl(response, handle_event)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'{self.options.baseUri}{url}', data=form_data) as response:
                    return await response.json()


# Options

class BaseAgentExecutionOptions(BaseModel):
    pass


class AgentExecutionOptionsNonStreaming(BaseAgentExecutionOptions):
    stream: Optional[bool] = False


class AgentExecutionOptionsStreaming(BaseAgentExecutionOptions):
    stream: bool = True


AgentExecutionOptions = Union[AgentExecutionOptionsNonStreaming, AgentExecutionOptionsStreaming]


# Node definition list

class NodeDefinitionListResponse(BaseModel):
    nodes: list[NodeDefinition]


# Node definition category list

class AgentCategorySchema(BaseModel):
    name: AgentCategory
    title: str


class AgentSubcategorySchema(BaseModel):
    name: AgentSubcategory
    title: str
    description: str
    category: AgentCategory


class AgentCategoryListResponse(BaseResponse):
    categories: list[AgentCategorySchema]
    subcategories: list[AgentSubcategorySchema]


# Agent execute

class BaseNonStreamingRequest(BaseModel):
    stream: Optional[bool] = False


class BaseStreamingRequest(BaseModel):
    stream: bool = True


class SingleNodeExecuteRequest(BaseModel):
    nodeName: str
    inputs: Dict[str, Any]
    stream: Optional[bool] = None


class SingleNodeExecuteStreamingRequest(SingleNodeExecuteRequest):
    stream: bool = True


class SingleNodeExecuteNonStreamingRequest(SingleNodeExecuteRequest):
    stream: Optional[bool] = False


class AgentExecuteRequest(BaseModel):
    inputs: Dict[str, Any]
    stream: Optional[bool] = None


class AgentExecuteStreamingRequest(AgentExecuteRequest):
    stream: bool = True


class AgentExecuteNonStreamingRequest(AgentExecuteRequest):
    stream: Optional[bool] = False


class AgentExecuteInlineRequest(BaseModel):
    inputs: Dict[str, Any]
    pipeline: InlineAgent
    stream: Optional[bool] = None


class AgentExecuteInlineStreamingRequest(AgentExecuteInlineRequest):
    stream: bool = True


class AgentExecuteInlineNonStreamingRequest(AgentExecuteInlineRequest):
    stream: Optional[bool] = False


class AgentExecuteNonStreamingResponse(BaseResponse):
    executionId: str
