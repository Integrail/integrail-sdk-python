from pydantic import BaseModel, Field
from typing import List

class Embedding(BaseModel):
    id: str = Field(alias="_id")
    embeddedDescription: str
    fullDescription: str
    embedding: List[float]
