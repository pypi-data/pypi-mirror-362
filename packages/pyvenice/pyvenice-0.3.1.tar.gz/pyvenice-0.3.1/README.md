# PyVenice

[![Python Version](https://img.shields.io/pypi/pyversions/pyvenice)](https://pypi.org/project/pyvenice/)
[![PyPI Version](https://img.shields.io/pypi/v/pyvenice)](https://pypi.org/project/pyvenice/)
[![License](https://img.shields.io/github/license/TheLustriVA/PyVenice)](https://github.com/TheLustriVA/PyVenice/blob/main/LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/TheLustriVA/PyVenice/tests.yml?branch=main&label=tests)](https://github.com/TheLustriVA/PyVenice/actions)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/charliermarsh/ruff)

A comprehensive Python client library for the Venice.ai API with automatic parameter validation, type safety, and support for all endpoints.

![PyVenice Banner](https://i.imgur.com/OsAkjoQ.png)

## ✨ Features

- 🔧 **Automatic Parameter Validation** - Removes unsupported parameters based on model capabilities
- 🛡️ **Full Type Safety** - Pydantic models for all requests and responses  
- 📡 **Complete API Coverage** - All 16 Venice.ai endpoints implemented
- ⚡ **Async Support** - Both synchronous and asynchronous clients
- 🌊 **Streaming Responses** - Efficient streaming for chat completions and audio
- 🔒 **Secure by Default** - HTTPS only, credentials stay local
- ⚙️ **Zero Configuration** - Sensible defaults with full customization
- 🧪 **Thoroughly Tested** - 82% test coverage with comprehensive test suite

Looking for Venice.ai access? Consider using my referreal code [https://venice.ai/chat?ref=0Y4qyR](https://venice.ai/chat?ref=0Y4qyR) or register at [venice.ai](https://venice.ai)

## 📦 Installation

```bash
pip install pyvenice
```

For development:

```bash
pip install pyvenice[dev]
```

### Troubleshooting Installation

If you encounter build errors (especially on ARM64 Android/Termux), see our [Installation Troubleshooting Guide](docs/INSTALLATION_TROUBLESHOOTING.md).

## 🚀 Quick Start

```python
from pyvenice import VeniceClient, ChatCompletion

# Initialize client (uses VENICE_API_KEY env var by default)
client = VeniceClient()

# Create a chat completion
chat = ChatCompletion(client)
response = chat.create(
    model="venice-uncensored",
    messages=[{"role": "user", "content": "Hello, Venice!"}]
)

print(response.choices[0].message.content)
```

## 💡 Usage Examples

### Chat Completions with Streaming

```python
from pyvenice import VeniceClient, ChatCompletion

client = VeniceClient(api_key="your-api-key")
chat = ChatCompletion(client)

# Stream responses
for chunk in chat.create_streaming(
    model="venice-coder",
    messages=[{"role": "user", "content": "Write a Python function"}],
    temperature=0.7
):
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Image Generation

```python
from pyvenice import VeniceClient, ImageGeneration

client = VeniceClient()
image_gen = ImageGeneration(client)

response = image_gen.generate(
    prompt="A serene lake at sunset",
    model="flux-schnell",
    width=1024,
    height=1024,
    steps=4
)

# Save the image
import base64
image_data = base64.b64decode(response.images[0])
with open("sunset.png", "wb") as f:
    f.write(image_data)
```

### Automatic Parameter Validation

PyVenice automatically removes parameters that aren't supported by specific models:

```python
# This won't cause an error even if venice-uncensored doesn't support parallel_tool_calls
response = chat.create(
    model="venice-uncensored",
    messages=[{"role": "user", "content": "Hello!"}],
    parallel_tool_calls=True  # Automatically removed if unsupported
)
```

### Async Support

```python
import asyncio
from pyvenice import VeniceClient, ChatCompletion

async def main():
    client = VeniceClient()
    chat = ChatCompletion(client)
    
    response = await chat.acreate(
        model="venice-coder",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

## 🎯 Supported Endpoints

- 💬 **Chat Completions** - `/chat/completions` with streaming and web search
- 🎨 **Image Generation** - `/image/generate`, `/images/generations`
- 🔍 **Image Upscaling** - `/image/upscale`
- 🔊 **Text to Speech** - `/audio/speech` with streaming
- 📊 **Embeddings** - `/embeddings`
- 🤖 **Model Management** - `/models`, `/models/traits`
- 🔑 **API Keys** - `/api_keys`, rate limits, and web3 key generation
- 👤 **Characters** - `/characters` for character-based interactions
- 💰 **Billing** - `/billing/usage` with pagination

## ⚙️ Configuration

### Environment Variables

```bash
export VENICE_API_KEY="your-api-key"
export VENICE_BASE_URL="https://api.venice.ai/api/v1"  # Optional
```

### Client Configuration

```python
client = VeniceClient(
    api_key="your-api-key",
    base_url="https://api.venice.ai/api/v1",
    timeout=30.0,
    max_retries=3
)
```

## 🧪 Testing

The test suite is included with the package for verification:

```bash
# Basic installation (no test dependencies)
pip install pyvenice

# Installation with test dependencies
pip install pyvenice[test]

# Run tests after installing with [test]
pytest -m "not integration"  # Unit tests only (no API key needed)
pytest --cov=pyvenice       # With coverage

# For development (includes test + dev tools)
pip install -e .[dev]
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

```bash
# Setup development environment
git clone https://github.com/TheLustriVA/PyVenice.git
cd PyVenice
pip install -e .[dev]

# Run tests before submitting PR
pytest
black .
ruff check .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

PyVenice prioritizes security:

- All communications use HTTPS with certificate verification
- API keys are never logged or included in error messages  
- No telemetry or data collection
- Minimal dependencies, all well-maintained and audited
- Input validation prevents injection attacks

For security concerns, please email [kieran@bicheno.me] or open an issue on GitHub

## 📚 Documentation

For detailed documentation, visit [our docs](https://github.com/TheLustriVA/PyVenice#readme) or check out the [examples](src/) directory.

## 🙏 Acknowledgments

Built with ❤️ using:

- [httpx](https://github.com/encode/httpx) - Modern HTTP client
- [pydantic](https://github.com/pydantic/pydantic) - Data validation
- [Venice.ai](https://venice.ai) - The underlying API

## 📈 Project Status

PyVenice is under active development. We follow [semantic versioning](https://semver.org/) and maintain backwards compatibility for all minor releases.

[![Star History Chart](https://api.star-history.com/svg?repos=TheLustriVA/PyVenice&type=Date)](https://star-history.com/#TheLustriVA/PyVenice&Date)
