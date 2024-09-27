from pydantic import BaseModel, RootModel
from typing import Dict, List, Union

from .data import ExternalService, TypeName

class BooleanValue(BaseModel):
    type: TypeName = TypeName.BOOLEAN
    value: bool

class NumberValue(BaseModel):
    type: TypeName = TypeName.NUMBER
    value: float

class IntegerValue(BaseModel):
    type: TypeName = TypeName.INTEGER
    value: int

class StringValue(BaseModel):
    type: TypeName = TypeName.STRING
    value: str

class VectorValue(BaseModel):
    type: TypeName = TypeName.VECTOR
    value: List[float]

class ObjectValue(BaseModel):
    type: TypeName = TypeName.OBJECT
    value: Dict[str, 'Value']

class ListValue(BaseModel):
    type: TypeName = TypeName.LIST
    value: List['Value']

class DictValue(BaseModel):
    type: TypeName = TypeName.DICT
    value: Dict[str, 'Value']

class UrlImageValue(BaseModel):
    type: TypeName = TypeName.IMAGE
    url: str

class Base64ImageValue(BaseModel):
    type: TypeName = TypeName.IMAGE
    base64: str

class ImageValue(BaseModel):
    type: TypeName = TypeName.IMAGE
    url: Union[str, None] = None
    base64: Union[str, None] = None

class VideoValue(BaseModel):
    type: TypeName = TypeName.VIDEO
    url: str

class AudioValue(BaseModel):
    type: TypeName = TypeName.AUDIO
    url: str

class ThreeDimensionalValue(BaseModel):
    type: TypeName = TypeName.THREE_DIMENSIONAL
    url: str

class FileValue(BaseModel):
    type: TypeName = TypeName.FILE
    url: str

class AuthTokenValue(BaseModel):
    type: TypeName = TypeName.AUTH_TOKEN
    service: ExternalService
    value: str

ValueUnion = Union[
    BooleanValue,
    NumberValue,
    IntegerValue,
    StringValue,
    VectorValue,
    ObjectValue,
    ListValue,
    DictValue,
    UrlImageValue,
    Base64ImageValue,
    VideoValue,
    AudioValue,
    ThreeDimensionalValue,
    FileValue,
    AuthTokenValue,
]

class Value(RootModel):
    root: ValueUnion

# To handle forward references
ObjectValue.update_forward_refs()
ListValue.update_forward_refs()
DictValue.update_forward_refs()
