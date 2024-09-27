from pydantic import BaseModel
from typing import Optional

class VectorMemory(BaseModel):
    name: str
    status: str
    colName: str
    embedderId: str
    indexName: Optional[str] = None
    vectorFieldName: str
    embeddedTextFieldName: str
    fullTextFieldName: str
