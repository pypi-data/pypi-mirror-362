# Verifik.io Python SDK

[![PyPI version](https://badge.fury.io/py/verifikio-sdk.svg)](https://badge.fury.io/py/verifikio-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/verifikio-sdk.svg)](https://pypi.org/project/verifikio-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for [Verifik.io](https://verifik.io) - Trust infrastructure for AI agent workflows.

Verifik.io provides secure, immutable audit trails for AI agents using blockchain-style verification. Perfect for teams building with CrewAI, LangChain, AutoGPT, and other AI frameworks who need SOC 2 / ISO27001 compliance.

## Features

- 🔐 **Secure audit logging** with automatic hash chaining
- 🚀 **Developer-friendly** - Get started in minutes
- 📊 **Chain verification** - Ensure data integrity
- 🔑 **Simple authentication** with API keys
- 🐍 **Python 3.7+** compatible
- 📦 **Minimal dependencies** - Only requires `requests`

## Installation

```bash
pip install verifikio-sdk
```

## Quick Start

```python
from verifikio import VerifikClient

# Initialize client with your API key
client = VerifikClient(api_key="verifik_live_abc123...")

# Log an AI agent event
response = client.log_event(
    agent_name="data_processor",
    action="process_customer_data",
    inputs={"customer_id": "cust_123", "data_type": "profile"},
    outputs={"status": "processed", "record_count": 1},
    metadata={"processing_time": "1.2s"},
    workflow_id="workflow_456",
    status="success"
)

print(f"Audit log created: {response['id']}")
print(f"Hash: {response['hash']}")
```

## API Reference

### VerifikClient

#### `__init__(api_key, base_url="https://api.verifik.io", timeout=30)`

Create a new Verifik.io client instance.

**Parameters:**
- `api_key` (str): Your Verifik.io API key (format: `verifik_live_*`)
- `base_url` (str, optional): Base URL for the API
- `timeout` (int, optional): Request timeout in seconds

```python
client = VerifikClient(api_key="verifik_live_abc123...")
```

#### `log_event(agent_name, action, **kwargs)`

Create a new audit log entry.

**Parameters:**
- `agent_name` (str): Name/identifier of the AI agent or service
- `action` (str): The action that was performed
- `inputs` (dict, optional): Input data/parameters for the action
- `outputs` (dict, optional): Output data/results from the action
- `metadata` (dict, optional): Additional metadata about the event
- `workflow_id` (str, optional): Workflow or session identifier
- `status` (str, optional): Status of the action (e.g., "success", "error", "pending")

**Returns:** `dict` - The created audit log entry

```python
response = client.log_event(
    agent_name="email_agent",
    action="send_notification",
    inputs={"recipient": "user@example.com"},
    outputs={"message_id": "msg_123"},
    status="success"
)
```

#### `get_logs(limit=50, offset=0, workflow_id=None)`

Retrieve audit logs with pagination.

**Parameters:**
- `limit` (int, optional): Number of logs to return (max 100)
- `offset` (int, optional): Number of logs to skip
- `workflow_id` (str, optional): Filter by workflow ID

**Returns:** `dict` - Paginated list of audit logs

```python
logs = client.get_logs(limit=20, offset=0)
for log in logs['logs']:
    print(f"Agent: {log['agentId']}, Action: {log['action']}")
```

#### `verify_chain()`

Verify the integrity of the audit log chain.

**Returns:** `dict` - Verification results

```python
verification = client.verify_chain()
print(f"Chain integrity: {verification['isValid']}")
```

#### `get_stats()`

Get account statistics and metrics.

**Returns:** `dict` - Account statistics

```python
stats = client.get_stats()
print(f"Total logs: {stats['totalLogs']}")
print(f"Chain integrity: {stats['chainIntegrity']}%")
```

## Framework Examples

### CrewAI Integration

```python
from verifikio import VerifikClient
from crewai import Agent, Task, Crew

# Initialize Verifik.io client
verifik = VerifikClient(api_key="verifik_live_abc123...")

# Create your CrewAI agents
researcher = Agent(
    role='Research Analyst',
    goal='Analyze market trends',
    backstory='Expert in market analysis'
)

# Custom callback to log CrewAI events
def log_crew_event(agent_name, action, inputs=None, outputs=None, status="success"):
    verifik.log_event(
        agent_name=agent_name,
        action=action,
        inputs=inputs,
        outputs=outputs,
        metadata={"framework": "crewai"},
        status=status
    )

# Log when agent starts task
log_crew_event("research_analyst", "start_analysis", {"topic": "AI market"})

# ... run your CrewAI workflow ...

# Log completion
log_crew_event("research_analyst", "complete_analysis", 
              outputs={"findings": "Market growing 40% YoY"})
```

### LangChain Integration

```python
from verifikio import VerifikClient
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler

verifik = VerifikClient(api_key="verifik_live_abc123...")

class VerifikCallback(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        verifik.log_event(
            agent_name="langchain_agent",
            action="chain_start",
            inputs=inputs,
            metadata={"chain_type": serialized.get("name", "unknown")}
        )
    
    def on_chain_end(self, outputs, **kwargs):
        verifik.log_event(
            agent_name="langchain_agent",
            action="chain_end",
            outputs=outputs,
            status="success"
        )

# Use the callback in your LangChain
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[VerifikCallback()])
```

## Error Handling

The SDK includes comprehensive error handling:

```python
from verifikio import VerifikClient, AuthenticationError, ValidationError, APIError

client = VerifikClient(api_key="verifik_live_abc123...")

try:
    response = client.log_event(
        agent_name="test_agent",
        action="test_action"
    )
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Context Manager Support

The client supports context manager protocol for automatic cleanup:

```python
with VerifikClient(api_key="verifik_live_abc123...") as client:
    client.log_event(
        agent_name="context_agent",
        action="test_action"
    )
# Client session automatically closed
```

## Getting Your API Key

1. Sign up at [verifik.io](https://verifik.io)
2. Go to your Settings page
3. Generate a new API key
4. Copy the key (format: `verifik_live_...`)

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=verifikio
```

### Code Quality

```bash
# Format code
black verifikio/

# Lint code
flake8 verifikio/

# Type checking
mypy verifikio/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 **Email**: support@verifik.io
- 📖 **Documentation**: https://docs.verifik.io
- 🐛 **Bug Reports**: https://github.com/verifik-io/verifikio-python/issues
- 💬 **Community**: https://discord.gg/verifik

## Changelog

### 1.0.0 (2024-01-14)
- Initial release
- Core audit logging functionality
- Chain verification
- Full API coverage
- Python 3.7+ support