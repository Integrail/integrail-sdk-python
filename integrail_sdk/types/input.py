from pydantic import RootModel
from typing import Any, List, Optional

from .data import Type
from .fail_mode import FailMode

class InputMetadata(Type):
    name: str
    title: str
    description: Optional[str] = None
    default: Optional[Any] = None
    advanced: Optional[bool] = None
    nsfw: Optional[bool] = None
    hidden: Optional[bool] = None
    failMode: Optional[FailMode] = None

class InputsMetadata(RootModel):
    root: List[InputMetadata]