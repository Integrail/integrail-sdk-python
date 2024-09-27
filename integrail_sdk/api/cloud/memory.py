from pydantic import BaseModel
from typing import List, Optional

from integrail_sdk.api.base import BaseApi, BaseResponse
from integrail_sdk.types.embedding import Embedding

class CloudMemoryApi(BaseApi):
    async def list(self, account_id: str, store_id: str) -> 'MemoryListResponse':
        response = await self.http_get(f"api/{account_id}/memory/{store_id}")
        json_data = await response.json()
        return MemoryListResponse.model_validate(json_data)

    async def upload(self, account_id: str, store_id: str, payload: 'MemoryUploadRequest') -> None:
        await self.http_post(f"api/{account_id}/memory/{store_id}", payload.model_dump(by_alias=True))

    async def delete(self, account_id: str, store_id: str, item_id: str) -> None:
        await self.http_delete(f"api/{account_id}/memory/{store_id}/{item_id}")

class MemoryListResponse(BaseResponse):
    items: List[Embedding]

class MemoryUploadItem(BaseModel):
    input: str
    inputFull: Optional[str] = None

class MemoryUploadRequest(BaseModel):
    items: List[MemoryUploadItem]