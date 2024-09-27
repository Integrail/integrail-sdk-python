import aiohttp
import asyncio
import json

async def jsonl(response: aiohttp.ClientResponse, cb):
    buffer = ""

    async def flush():
        nonlocal buffer
        if buffer.strip():
            lines = buffer.split("\n")
            for line in lines[:-1]:
                parsed = json.loads(line)
                await cb(parsed)
            # await asyncio.gather(*[cb(json.loads(line)) for line in lines[:-1]])
            buffer = lines[-1] if lines else ""

    async for chunk in response.content.iter_any():
        chunk_text = chunk.decode('utf-8')
        buffer += chunk_text
        await flush()

    buffer += "\n"  # flush last line
    await flush()
