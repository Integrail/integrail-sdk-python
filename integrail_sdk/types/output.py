from pydantic import RootModel
from typing import Any, List, Optional

from .data import Type

class OutputMetadata(Type):
    name: str
    title: str
    description: Optional[str] = None
    default: Optional[Any] = None
    saveHistory: Optional[bool] = None

class OutputsMetadata(RootModel):
    root: List[OutputMetadata]