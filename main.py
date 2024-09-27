import asyncio

import integrail_sdk

async def main():
    api = integrail_sdk.IntegrailCloudApi({
        'baseUri': 'http://localhost:8000',
        'apiToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI1S3ZhRkh3ek1hYmkyRDZGRyIsImVtYWlsIjoiZGFuaWlsLmtAaW50ZWdyYWlsLmFpIiwiYXBwIjoiaW50ZWdyYWlsLmFpIiwiaWF0IjoxNzI3MzU5NDk4LCJleHAiOjE3Mjc0NDU4OTh9.QOAP5GsXsK28KKfUQIi2WbA9-bPKP0zBMTqTTEhsDyg'
    })
    r = await api.node.list()
    print(r.model_dump_json())
    api.agent.execute()

asyncio.run(main())