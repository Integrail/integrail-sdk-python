# Integrail SDK

## Usage

Below is an example of how to initialize the `IntegrailCloudApi` and use streaming versions of its `agent.execute` and `agent.execute_multipart` methods.

### Initializing IntegrailCloudApi

```python
from integrail_sdk import IntegrailCloudApi

# Initialize the API with options
options = {
    "apiToken": "your_api_key",
}
cloud_api = IntegrailCloudApi(options)
```

### Using `agent.execute`

```python
import asyncio
from typing import Optional

from integrail_sdk.types import ExecutionEvent, AgentExecution
from integrail_sdk.api import CloudAgentExecuteStreamingRequest

def on_event(event: ExecutionEvent, execution: Optional[AgentExecution]):
    print(f"Event: {event}, Execution: {execution}")

def on_finish(execution: Optional[AgentExecution]):
    print(f"Finished: {execution}")

async def main():
    await cloud_api.agent.execute(
        "agent123",
        "account123",
        CloudAgentExecuteStreamingRequest(
            inputs={"param1": "value1"},
            stream=True,
        ),
        on_event,
        on_finish
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

### Using `agent.execute_multipart`

```python
import asyncio
from typing import Optional

from integrail_sdk.types import ExecutionEvent, AgentExecution
from integrail_sdk.api import CloudAgentExecuteStreamingRequest

def on_event(event: ExecutionEvent, execution: Optional[AgentExecution]):
    print(f"Event: {event}, Execution: {execution}")

def on_finish(execution: Optional[AgentExecution]):
    print(f"Finished: {execution}")

async def main():  
    await cloud_api.agent.execute_multipart(
        "agent123",
        "account123",
        CloudAgentExecuteStreamingRequest(
            inputs={"param1": "value1"},
            stream=True,
        ),
        {"file1": open("data.csv", "rb")},
        on_event,
        on_finish
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

## License

This project is licensed under the MIT License. See the `LICENSE.txt` file for more details.