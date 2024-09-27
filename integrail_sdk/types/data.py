from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union
from enum import Enum

class TypeName(str, Enum):
    BOOLEAN = "boolean"
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    ENUM = "enum"
    VECTOR = "vector"
    OBJECT = "object"
    LIST = "list"
    DICT = "dict"
    ONE_OF = "oneOf"
    ANY = "any"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    THREE_DIMENSIONAL = "threeDimensional"
    FILE = "file"
    NODE_CALL = "nodeCall"
    CALL = "call"
    AUTH_TOKEN = "authToken"

class ExternalService(str, Enum):
    GOOGLE = "google"
    WIX = "wix"
    CLICKUP = "clickup"
    TELEGRAM = "telegram"
    OPENAI = "openai"
    OLLAMA = "ollama"
    ANTHROPIC = "anthropic"
    ANYSCALE = "anyscale"
    FIREWORKS = "fireworks"
    GOOGLE_VERTEX = "google_vertex"
    STABILITY = "stability"

class InputRef(BaseModel):
    ref: str

class TypePrimitive(BaseModel):
    type: TypeName
    min: Optional[float] = None
    max: Optional[float] = None
    truncate: Optional[bool] = None
    variants: Optional[List[str]] = None
    size: Optional[int] = None

class TypeComplex(BaseModel):
    type: TypeName
    properties: Optional[Dict[str, 'Type']] = None
    elements: Optional['Type'] = None
    size: Optional[Union[int, InputRef]] = None
    defaultLimit: Optional[int] = None
    min: Optional[int] = None
    max: Optional[int] = None
    variants: Optional[List['Type']] = None

class TypeMedia(BaseModel):
    type: TypeName

class TypeRef(BaseModel):
    type: TypeName

class TypeExternal(BaseModel):
    type: TypeName
    service: ExternalService

class Type(BaseModel):
    type: TypeName
    optional: Optional[bool] = None
    properties: Optional[Dict[str, 'Type']] = None
    elements: Optional['Type'] = None
    size: Optional[Union[int, InputRef]] = None
    defaultLimit: Optional[int] = None
    min: Optional[int] = None
    max: Optional[int] = None
    variants: Optional[Union[List['Type'], List[str]]] = None
    service: Optional[ExternalService] = None
    truncate: Optional[bool] = None
    ref: Optional[str] = None

    @staticmethod
    def to_json_schema(t: 'Type') -> Dict[str, Any]:
        if t.type == TypeName.BOOLEAN:
            return {"type": "boolean"}
        elif t.type == TypeName.NUMBER:
            return {"type": "number", "minimum": t.min, "maximum": t.max}
        elif t.type == TypeName.INTEGER:
            return {"type": "integer", "minimum": t.min, "maximum": t.max}
        elif t.type == TypeName.STRING:
            return {"type": "string", "minLength": t.min, "maxLength": t.max}
        elif t.type == TypeName.ENUM:
            return {"type": "string", "enum": t.variants}
        elif t.type == TypeName.VECTOR:
            return {"type": "array", "items": {"type": "number"}, "minItems": t.size, "maxItems": t.size}
        elif t.type == TypeName.OBJECT:
            return {
                "type": "object",
                "properties": {name: Type.to_json_schema(type) for name, type in t.properties.items()}
            }
        elif t.type == TypeName.LIST:
            return {
                "type": "array",
                "items": Type.to_json_schema(t.elements),
                "minItems": t.min,
                "maxItems": t.max
            }
        elif t.type == TypeName.DICT:
            return {
                "type": "object",
                "additionalProperties": Type.to_json_schema(t.elements)
            }
        elif t.type == TypeName.ONE_OF:
            return {"oneOf": [Type.to_json_schema(variant) for variant in t.variants]}
        elif t.type == TypeName.ANY:
            return {}
        elif t.type == TypeName.IMAGE:
            return {
                "oneOf": [
                    {"type": "object", "properties": {"url": {"type": "string"}}},
                    {"type": "object", "properties": {"base64": {"type": "string"}}}
                ]
            }
        elif t.type == TypeName.AUDIO:
            return {"type": "object", "properties": {"url": {"type": "string"}}}
        elif t.type == TypeName.VIDEO:
            return {"type": "object", "properties": {"url": {"type": "string"}}}
        elif t.type == TypeName.THREE_DIMENSIONAL:
            return {"type": "object", "properties": {"url": {"type": "string"}}}
        elif t.type == TypeName.FILE:
            return {
                "type": "object",
                "properties": {"url": {"type": "string"}, "fileName": {"type": "string"}}
            }
        elif t.type == TypeName.NODE_CALL:
            return {
                "type": "object",
                "properties": {"nodeId": {"type": "string"}, "inputs": {"type": "object"}}
            }
        elif t.type == TypeName.CALL:
            return {
                "type": "object",
                "properties": {"inputs": {"type": "object"}}
            }
        elif t.type == TypeName.AUTH_TOKEN:
            return {"type": "object"}

# To handle forward references
Type.update_forward_refs()
TypeComplex.update_forward_refs()