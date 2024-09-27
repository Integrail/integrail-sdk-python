from pydantic import BaseModel
from typing import Any, List, Optional

class NodeInput(BaseModel):
    name: str
    value: Optional[Any] = None

class Node(BaseModel):
    id: str
    name: str
    inputs: Optional[List[NodeInput]] = None
    fallbackOutputs: Optional[List[NodeInput]] = None
    call: Optional[dict] = None

    callDescription: Optional[str] = None  # Deprecated
    inputsRef: Optional[str] = None  # Deprecated

class NodeSelector(BaseModel):
    nodeId: str