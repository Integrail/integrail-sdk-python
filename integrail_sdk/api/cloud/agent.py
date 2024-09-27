from pydantic import BaseModel
from typing import Any, Dict, Optional, Union, Callable
import aiohttp

from integrail_sdk.types.execution import AgentExecution, ExecutionEvent
from integrail_sdk.api.base import BaseApi
from integrail_sdk.api.common.agent import (
    AgentCategoryListResponse,
    AgentExecuteNonStreamingResponse,
    BaseAgentApi,
)

class CloudAgentApi(BaseAgentApi):
    @property
    def multi(self) -> 'CloudAgentApi':
        return self

    async def execute(
        self,
        agent_id: str,
        account_id: str,
        payload: 'CloudAgentExecuteRequest',
        on_event: Optional[Callable[[ExecutionEvent, Optional[AgentExecution]], Any]] = None,
        on_finish: Optional[Callable[[Optional[AgentExecution]], Any]] = None,
    ) -> Union[AgentExecuteNonStreamingResponse, aiohttp.ClientTimeout]:
        return await self.wrap_execution(
            f"api/{account_id}/agent/{agent_id}/execute",
            payload.model_dump(by_alias=True),
            on_event,
            on_finish,
        )

    async def execute_multipart(
        self,
        agent_id: str,
        account_id: str,
        payload: 'CloudAgentExecuteRequest',
        files: Dict[str, Any],
        on_event: Optional[Callable[[ExecutionEvent, Optional[AgentExecution]], Any]] = None,
        on_finish: Optional[Callable[[Optional[AgentExecution]], Any]] = None,
    ) -> Union[AgentExecuteNonStreamingResponse, aiohttp.ClientTimeout]:
        return await self.wrap_execution_multipart(
            f"api/{account_id}/agent/{agent_id}/execute/multipart",
            payload.model_dump(by_alias=True),
            files,
            on_event,
            on_finish,
        )

class CloudCategoryApi(BaseApi):
    async def list(self) -> AgentCategoryListResponse:
        response = await self.http_get("api/node/category/list")
        return AgentCategoryListResponse.model_validate(await response.json())

class CloudAgentExecuteRequest(BaseModel):
    inputs: Dict[str, Any]
    stream: Optional[bool] = None
    externalId: Optional[str] = None

class CloudAgentExecuteStreamingRequest(CloudAgentExecuteRequest):
    stream: bool = True

class CloudAgentExecuteNonStreamingRequest(CloudAgentExecuteRequest):
    stream: Optional[bool] = False