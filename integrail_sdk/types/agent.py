from pydantic import BaseModel, RootModel, Field
from typing import List, Optional, Dict, Union

from .data import Type
from .node import Node
from .node_execution import NodeExecutionState

class AgentInput(Type):
    name: str
    saveHistory: Optional[bool] = None

class AgentOutput(Type):
    name: str
    value: str
    saveHistory: Optional[bool] = None

class InlineAgent(BaseModel):
    inputs: List[AgentInput]
    outputs: List[AgentOutput]
    nodes: List[Node]
    mock: Optional[Dict[str, NodeExecutionState]] = None

class AgentIntegrationToken(BaseModel):
    tokenId: str

class AgentIntegrations(RootModel):
    root: Dict[str, List[AgentIntegrationToken]]

class Agent(InlineAgent):
    id: Optional[str] = Field(alias="_id", default=None)
    version: Optional[Union[str, int]] = None
    integrations: Optional[AgentIntegrations] = None
    accountId: Optional[str] = None

class CloudAgent(Agent):
    isActive: bool