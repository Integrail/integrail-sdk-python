from pydantic import BaseModel
from typing import Dict, Optional

class ExecutionStats(BaseModel):
    cost: Optional[float] = None
    inputTokens: Optional[int] = None
    outputTokens: Optional[int] = None

class AgentExecutionStats(ExecutionStats):
    count: Optional[int] = None

class AggregatedExecutionStats(BaseModel):
    byAgent: Dict[str, AgentExecutionStats]
    total: ExecutionStats