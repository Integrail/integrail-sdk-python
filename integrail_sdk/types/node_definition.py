from pydantic import BaseModel, HttpUrl, Field
from typing import Any, Optional
from enum import Enum
from datetime import date

from .category import AgentCategory, AgentSubcategory
from .input import InputsMetadata
from .output import OutputsMetadata

class NodeDefinitionAvailabilityStatus(str, Enum):
    ACTIVE = "active"      # Model is fully supported and recommended for use.
    LEGACY = "legacy"      # Model no longer receives updates and may be deprecated in the future.
    DEPRECATED = "deprecated"  # Model is not recommended for use, retirement date is assigned.

class NodeDefinitionAvailability(BaseModel):
    status: NodeDefinitionAvailabilityStatus
    message: Optional[str] = None
    deprecation: Optional[date] = None
    retirement: Optional[date] = None

class BaseNodeDefinition(BaseModel):
    name: str
    title: str
    shortId: Optional[str] = Field(None, max_length=5)
    description: Optional[str] = None
    url: Optional[HttpUrl] = None
    category: AgentCategory
    subcategory: Optional[AgentSubcategory] = None
    hidden: Optional[bool] = None
    availability: NodeDefinitionAvailability = Field(default_factory=lambda: NodeDefinitionAvailability(status=NodeDefinitionAvailabilityStatus.ACTIVE))
    metadata: Any

class NodeDefinition(BaseNodeDefinition):
    inputs: InputsMetadata
    outputs: OutputsMetadata
