from pydantic import BaseModel, HttpUrl
from typing import Union

from .data import TypeName

class Image(BaseModel):
    type: TypeName = TypeName.IMAGE
    url: Union[HttpUrl, None] = None
    base64: Union[str, None] = None

    class Config:
        validate_assignment = True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not (v.url or v.base64):
            raise ValueError("Either 'url' or 'base64' must be provided")
        return v

class Audio(BaseModel):
    type: TypeName = TypeName.AUDIO
    url: HttpUrl

class Video(BaseModel):
    type: TypeName = TypeName.VIDEO
    url: HttpUrl

class File(BaseModel):
    type: TypeName = TypeName.FILE
    url: HttpUrl
    fileName: str

class ThreeD(BaseModel):
    type: TypeName = TypeName.THREE_DIMENSIONAL
    url: HttpUrl