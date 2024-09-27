from typing import Any, Optional, Union, Callable
import aiohttp

from integrail_sdk.types import ExecutionEvent, AgentExecution
from integrail_sdk.api.common.agent import (
    BaseAgentApi,
    NodeDefinitionListResponse,
    AgentExecuteNonStreamingResponse,
    SingleNodeExecuteRequest,
)

class CloudNodeApi(BaseAgentApi):
    async def list(self) -> NodeDefinitionListResponse:
        response = await self.http_get("api/node/list")
        return NodeDefinitionListResponse.model_validate(await response.json(), strict=False)

    async def execute(
        self,
        payload: SingleNodeExecuteRequest,
        on_event: Optional[Callable[[ExecutionEvent, Optional[AgentExecution]], Any]] = None,
        on_finish: Optional[Callable[[Optional[AgentExecution]], Any]] = None,
    ) -> Union[AgentExecuteNonStreamingResponse, aiohttp.ClientTimeout]:
        return await self.wrap_execution("api/node/execute", payload.model_dump(by_alias=True), on_event, on_finish)