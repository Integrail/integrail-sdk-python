from pydantic import BaseModel, HttpUrl, Field
from typing import Any, Optional
import aiohttp

class ApiOptions(BaseModel):
    baseUri: HttpUrl = Field(default="https://cloud.integrail.ai")
    apiToken: str

class BaseApi:
    def __init__(self, params: dict | ApiOptions):
        if isinstance(params, dict):
            params = ApiOptions(**params)
        self.options = params

    async def fetch(self, path: str, init: Optional[dict] = None) -> aiohttp.ClientResponse:
        # raise ValueError(f"{self.options.baseUri}{path}")

        if not init:
            init = {}
        
        method = init.get('method', 'GET')
        json = init.get('json', None)
        headers = init.get('headers', {})
        headers['Authorization'] = f'Bearer {self.options.apiToken}'
        # headers = {**(init.get('headers') if init else {}), 'Authorization': f'Bearer {self.options.apiToken}'}

        session = aiohttp.ClientSession()
        # async with aiohttp.ClientSession() as session:
            # async with session.request(method, f"{self.options.baseUri}{path}", headers=headers, json=json) as response:
        response = await session.request(method, f"{self.options.baseUri}{path}", headers=headers, json=json)
        if 200 <= response.status < 300:
            # raise ValueError(await response.json())
            return response
        raise Exception(f"Request failed with status {response.status}")

    async def http_get(self, path: str) -> aiohttp.ClientResponse:
        return await self.fetch(path)

    async def http_post(self, path: str, body: Any) -> aiohttp.ClientResponse:
        return await self.fetch(path, {
            'method': 'POST',
            'json': body,
            'headers': {'Content-Type': 'application/json'}
        })

    async def http_delete(self, path: str) -> aiohttp.ClientResponse:
        return await self.fetch(path, {
            'method': 'DELETE'
        })

class BaseResponse(BaseModel):
    status: str = Field(default="ok")