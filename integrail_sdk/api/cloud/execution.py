from integrail_sdk.types import AgentExecution
from integrail_sdk.api.base import BaseResponse

class ExecutionStatusResponse(BaseResponse):
    execution: AgentExecution