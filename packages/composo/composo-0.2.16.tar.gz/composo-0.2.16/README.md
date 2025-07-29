# Composo Python SDK

A Python SDK for Composo evaluation services, providing both synchronous and asynchronous clients for evaluating LLM conversations with support for OpenAI and Anthropic formats.

## Features

- **Dual Client Support**: Both synchronous and asynchronous clients
- **Multiple LLM Provider Support**: Native support for OpenAI and Anthropic formats
- **Connection Pooling**: Optimized HTTP client with connection reuse
- **Retry Logic**: Exponential backoff with jitter for robust API calls
- **Type Safety**: Full type hints and Pydantic models
- **Context Managers**: Proper resource management with context managers

## Installation

```bash
pip install composo
```

## Quick Start

### Basic Usage

```python
from composo import Composo, AsyncComposo

# Initialize client
client = Composo(api_key="your-api-key")

# Evaluate messages
messages = [
    {"role": "user", "content": "What is machine learning?"},
    {"role": "assistant", "content": "Machine learning is..."}
]

criteria = ["Reward responses that provide accurate technical explanations"]

result = client.evaluate(messages=messages, criteria=criteria)
print(f"Score: {result.score}")
print(f"Explanation: {result.explanation}")
```

### Async Usage

```python
import asyncio
from composo import AsyncComposo

async def main():
    async with AsyncComposo(api_key="your-api-key") as client:
        result = await client.evaluate(
            messages=messages,
            criteria=criteria
        )
        print(f"Score: {result.score}")

asyncio.run(main())
```

### With LLM Results

```python
import openai
from composo import Composo

# Get response from OpenAI
openai_client = openai.OpenAI(api_key="your-openai-key")
openai_result = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What is machine learning?"}]
)

# Evaluate the response
composo_client = Composo(api_key="your-composo-key")
eval_result = composo_client.evaluate(
    messages=[{"role": "user", "content": "What is machine learning?"}],
    result=openai_result,
    criteria=["Reward accurate technical explanations"]
)
```

## Configuration

### Client Options

- `api_key` (required): Your Composo API key
- `base_url` (optional): Custom API endpoint (default: https://platform.composo.ai)
- `num_retries` (optional): Number of retry attempts (default: 1)
- `model_core` (optional): Specific model core for evaluation

### Logging

The SDK uses Python's standard logging module. Configure logging level:

```python
import logging
logging.getLogger("composo").setLevel(logging.INFO)
```

## Error Handling

The SDK provides specific exception types:

```python
from composo import (
    ComposoError,
    RateLimitError,
    MalformedError,
    APIError,
    AuthenticationError
)

try:
    result = client.evaluate(messages=messages, criteria=criteria)
except RateLimitError:
    print("Rate limit exceeded")
except AuthenticationError:
    print("Invalid API key")
except ComposoError as e:
    print(f"Composo error: {e}")
```

## Performance Optimization

- **Connection Pooling**: HTTP clients reuse connections for better performance
- **Context Managers**: Use context managers to properly close connections
- **Async Support**: Use async client for high-throughput scenarios