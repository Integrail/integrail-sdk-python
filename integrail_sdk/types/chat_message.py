from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from .value import Value

class ChatMessageRole(str, Enum):
    ASSISTANT = "assistant"
    USER = "user"

class ChatMessagePart(Value):
    __pydantic_extra__ = {'name': Optional[str]}

class ChatMessage(BaseModel):
    role: ChatMessageRole
    parts: List[ChatMessagePart]
