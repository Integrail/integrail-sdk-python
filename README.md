from integrail_sdk import CloudAgentExecuteStreamingRequest

# Integrail SDK

The Integrail SDK provides a set of tools for working with various data types and external services. It is built using Python and leverages the Pydantic library for data validation and serialization.

## Usage

Below is an example of how to initialize the `IntegrailCloudApi` and use its `agent.execute` and `agent.execute_multipart` methods with `inputs`, `on_event`, and `on_finish` callbacks.

### Initializing IntegrailCloudApi

```python
from integrail_sdk import IntegrailCloudApi

# Initialize the API with options
options = {
    "api_key": "your_api_key",
}
cloud_api = IntegrailCloudApi(options)
```

### Using `agent.execute`

```python
from typing import Optional

from integrail_sdk.types import ExecutionEvent, AgentExecution
from integrail_sdk.api import CloudAgentExecuteStreamingRequest

def on_event(event: ExecutionEvent, execution: Optional[AgentExecution]):
    print(f"Event: {event}, Execution: {execution}")

def on_finish(execution: Optional[AgentExecution]):
    print(f"Finished: {execution}")

cloud_api.agent.execute(
    "agent123",
    "account123",
    CloudAgentExecuteStreamingRequest(
        inputs={"param1": "value1"},
        stream=True,
    ),
    on_event,
    on_finish
)
```

### Using `agent.execute_multipart`

```python
from typing import Optional

from integrail_sdk.types import ExecutionEvent, AgentExecution
from integrail_sdk.api import CloudAgentExecuteStreamingRequest

def on_event(event: ExecutionEvent, execution: Optional[AgentExecution]):
    print(f"Event: {event}, Execution: {execution}")

def on_finish(execution: Optional[AgentExecution]):
    print(f"Finished: {execution}")

cloud_api.agent.execute_multipart(
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
```

## License

This project is licensed under the MIT License. See the `LICENSE.txt` file for more details.