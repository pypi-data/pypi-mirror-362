# langchain-iointelligence

[![PyPI version](https://badge.fury.io/py/langchain-iointelligence.svg)](https://badge.fury.io/py/langchain-iointelligence)
[![Python versions](https://img.shields.io/pypi/pyversions/langchain-iointelligence.svg)](https://pypi.org/project/langchain-iointelligence/)
[![License](https://img.shields.io/pypi/l/langchain-iointelligence.svg)](https://pypi.org/project/langchain-iointelligence/)
[![Downloads](https://pepy.tech/badge/langchain-iointelligence)](https://pepy.tech/project/langchain-iointelligence)

> **📦 [Available on PyPI](https://pypi.org/project/langchain-iointelligence/)** - Install with `pip install langchain-iointelligence`

## 📋 Feature Support Matrix

| Feature | Status | Notes |
|---------|-----------|-------|
| ✅ **Chat Model** | **Fully Supported** | Message-based interface with system/user/assistant roles |
| ✅ **Text LLM** | **Fully Supported** | Traditional prompt-response interface |
| ✅ **Sync Generation** | **Fully Supported** | Standard text generation with token usage tracking |
| ✅ **Error Handling** | **Production Ready** | Comprehensive error classification and retry logic |
| ✅ **Token Usage** | **Fully Supported** | `response.usage_metadata` access (0.2.1+) |
| ⚠️ **Streaming** | **Basic Support** | SSE token chunks; usage-at-end *coming soon* |
| ❌ **Function/Tool Calling** | **Not Supported** | Planned for future release |
| ❌ **Vision/Multimodal** | **Not Supported** | Text-only interface currently |
| ❌ **Embeddings** | **Not Supported** | Use dedicated embedding providers |

> **Note**: Non-core message roles default to `user`. Usage metadata always includes all required fields (`input_tokens`, `output_tokens`, `total_tokens`) with defaults of 0 when data unavailable.

**LangChain-compatible wrapper** for io Intelligence LLM API with **OpenAI-compatible interface**. Features both traditional Text LLM and modern Chat Model interfaces with comprehensive error handling, token usage tracking, and streaming support.

## 🚀 Key Features

* **🔄 Dual Interface Support**: Both `IOIntelligenceLLM` (text-based) and `IOIntelligenceChatModel` (message-based)
* **⚡ OpenAI-Compatible Interface**: Drop-in replacement with identical parameters and behavior
* **📡 Streaming Support**: Token-by-token streaming (usage-at-end coming soon)
* **🛡️ Production-Grade Reliability**: Automatic retries, detailed error classification, and robust fallbacks
* **🔀 Runtime Provider Switching**: Easy switching between OpenAI, Anthropic, and io Intelligence
* **📊 LangChain Token Tracking**: Standard `usage_metadata` with `input_tokens`/`output_tokens`/`total_tokens`
* **🎛️ Modern LangChain Integration**: Full support for `prompt | llm | parser` chains

## ⚙️ Installation

```bash
pip install langchain-iointelligence
```

## 🔐 Quick Setup

Create a `.env` file:

```env
IO_API_KEY=your_api_key_here
IO_API_URL=https://api.intelligence.io.solutions/api/v1/chat/completions
```

## 🎯 Quick Start

### **Modern Chat Model (Recommended)**

```python
from langchain_iointelligence import IOIntelligenceChat
from langchain_core.messages import HumanMessage

# Initialize with ChatGPT-compatible parameters
chat = IOIntelligenceChat(
    model="meta-llama/Llama-3.3-70B-Instruct",
    temperature=0.7,
    max_tokens=1000,
    timeout=30,
    max_retries=3
)

# Direct usage
messages = [HumanMessage(content="Explain quantum computing")]
response = chat.invoke(messages)
print(response.content)  # AIMessage content
print(response.usage_metadata)  # Token usage: input_tokens, output_tokens, total_tokens
```

### **Streaming Responses**

```python
from langchain_iointelligence import IOIntelligenceChat

chat = IOIntelligenceChat(streaming=True)
messages = [HumanMessage(content="Write a story about AI")]

# Real streaming with server-sent events
for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)
```

### **Model Discovery**

```python
from langchain_iointelligence import list_available_models, is_model_available

# List all available models
models = list_available_models()
print("Available models:", models)

# Check if specific model exists
if is_model_available("meta-llama/Llama-3.3-70B-Instruct"):
    print("Model is available!")
```

## 🔗 Advanced LangChain Integration

### **Modern Chain with Full Pipeline**

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_iointelligence import IOIntelligenceChat

# Complete modern pipeline
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert technical writer."),
    ("human", "Explain {topic} in {style} style, max {words} words.")
])

chat = IOIntelligenceChat(
    model="meta-llama/Llama-3.3-70B-Instruct",
    temperature=0.3
)

parser = StrOutputParser()

# Modern chain: prompt | chat | parser
chain = prompt | chat | parser

result = chain.invoke({
    "topic": "machine learning",
    "style": "beginner-friendly", 
    "words": "200"
})
print(result)
```

### **Runtime Provider Switching**

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic  
from langchain_iointelligence import IOIntelligenceChat

# Configure multiple providers
providers = {
    "openai": ChatOpenAI(model="gpt-4"),
    "anthropic": ChatAnthropic(model="claude-3-sonnet-20240229"),
    "iointelligence": IOIntelligenceChat(model="meta-llama/Llama-3.3-70B-Instruct")
}

# Runtime switching via configuration
configurable_chat = providers["openai"].configurable_alternatives(
    ConfigurableField(id="provider"),
    default_key="openai",
    **providers
)

# Switch provider at runtime
response = configurable_chat.invoke(
    "Hello world!",
    config={"configurable": {"provider": "iointelligence"}}
)
```

### **Production Fallback Configuration**

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_iointelligence import IOIntelligenceChat

# Multi-tier fallback system
primary = IOIntelligenceChat(
    model="meta-llama/Llama-3.3-70B-Instruct",
    timeout=10,
    max_retries=2
)

secondary = ChatOpenAI(model="gpt-4", timeout=15)
tertiary = ChatAnthropic(model="claude-3-sonnet-20240229")

# Automatic fallback chain
reliable_chat = primary.with_fallbacks([secondary, tertiary])

# Will automatically try alternatives on failure
response = reliable_chat.invoke("Complex analysis request")
```

### **Error Handling and Monitoring**

```python
from langchain_iointelligence import (
    IOIntelligenceChat,
    IOIntelligenceRateLimitError,
    IOIntelligenceServerError,
    IOIntelligenceAuthenticationError
)

chat = IOIntelligenceChat()

try:
    response = chat.invoke("Generate report")
    print(f"Success! Used {response.usage_metadata['total_tokens']} tokens")
    
except IOIntelligenceRateLimitError as e:
    print(f"Rate limited: {e}. Retry after: {e.retry_after}")
    
except IOIntelligenceServerError as e:
    print(f"Server error {e.status_code}: {e}")
    
except IOIntelligenceAuthenticationError:
    print("Invalid API key - check your credentials")
```

## 🛠️ Configuration Options

### **Complete Parameter Reference**

```python
from langchain_iointelligence import IOIntelligenceChat

chat = IOIntelligenceChat(
    # API Configuration
    api_key="your_key",                           # or use IO_API_KEY env var  
    api_url="https://api.example.com/v1/chat",    # or use IO_API_URL env var
    
    # Model Parameters (ChatGPT Compatible)
    model="meta-llama/Llama-3.3-70B-Instruct",   # Model identifier
    temperature=0.7,                              # Creativity (0.0-2.0)
    max_tokens=2000,                              # Response length limit
    
    # Reliability & Performance  
    timeout=30,                                   # Request timeout (seconds)
    max_retries=3,                                # Retry attempts
    retry_delay=1.0,                              # Initial retry delay
    streaming=True,                               # Enable real streaming
)
```

### **Available Models**

Check the latest models dynamically:

```python
from langchain_iointelligence import IOIntelligenceUtils

utils = IOIntelligenceUtils()
models = utils.list_models()

for model in models:
    print(f"Model: {model['id']}")
    if 'description' in model:
        print(f"  Description: {model['description']}")

# Get recommended models
recommended = utils.get_recommended_models()
print("Recommended models:", recommended)
```

Common models include:
- `meta-llama/Llama-3.3-70B-Instruct` (default, balanced performance)
- `meta-llama/Llama-3.1-405B-Instruct` (highest capability)
- `meta-llama/Llama-3.1-70B-Instruct` (fast and efficient)

## 🔌 API Compatibility

**Full OpenAI ChatCompletion API compatibility:**

```json
{
  "model": "meta-llama/Llama-3.3-70B-Instruct",
  "messages": [{"role": "user", "content": "Hello"}],
  "temperature": 0.7,
  "max_tokens": 1000,
  "stream": true,
  "stop": ["END"]
}
```

**Also supports legacy Text Completion format:**

```json
{
  "model": "meta-llama/Llama-3.3-70B-Instruct",
  "prompt": "Hello",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

## 🔍 Migration Guides

### **From OpenAI ChatGPT**

```python
# Before (OpenAI)
from langchain_openai import ChatOpenAI
chat = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000,
    timeout=30
)

# After (io Intelligence) - Same parameters!
from langchain_iointelligence import IOIntelligenceChat
chat = IOIntelligenceChat(
    model="meta-llama/Llama-3.3-70B-Instruct",
    temperature=0.7,
    max_tokens=1000, 
    timeout=30
)
```

### **From Anthropic Claude**

```python
# Before (Anthropic)
from langchain_anthropic import ChatAnthropic
chat = ChatAnthropic(model="claude-3-sonnet-20240229")

# After (io Intelligence)
from langchain_iointelligence import IOIntelligenceChat
chat = IOIntelligenceChat(model="meta-llama/Llama-3.3-70B-Instruct")

# Same interface - no code changes needed!
response = chat.invoke([HumanMessage(content="Hello")])
```

## ✅ Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=langchain_iointelligence --cov-report=html

# Test specific functionality
pytest tests/test_chat.py::TestIOIntelligenceChatModel::test_streaming -v
```

## 🚀 Advanced Examples

### **Batch Processing with Rate Limit Handling**

```python
import asyncio
from langchain_iointelligence import IOIntelligenceChat, IOIntelligenceRateLimitError

async def process_batch(prompts, chat):
    results = []
    for prompt in prompts:
        try:
            result = await chat.ainvoke(prompt)
            results.append(result)
        except IOIntelligenceRateLimitError:
            await asyncio.sleep(60)  # Wait for rate limit reset
            result = await chat.ainvoke(prompt)  # Retry
            results.append(result)
    return results
```

### **Custom Retry Logic**

```python
from langchain_iointelligence import IOIntelligenceChat

# Custom retry configuration
chat = IOIntelligenceChat(
    max_retries=5,
    retry_delay=2.0,  # Start with 2 second delays
    timeout=60        # Longer timeout for complex requests
)
```

### **Model Performance Comparison**

```python
from langchain_iointelligence import IOIntelligenceChat

models = [
    "meta-llama/Llama-3.3-70B-Instruct",
    "meta-llama/Llama-3.1-405B-Instruct",
    "meta-llama/Llama-3.1-70B-Instruct"
]

prompt = "Solve this math problem: 2x + 5 = 15"

for model in models:
    chat = IOIntelligenceChat(model=model)
    response = chat.invoke(prompt)
    print(f"Model {model}: {response.content}")
    print(f"Tokens used: {response.usage_metadata}")
```

## 🔧 Development

```bash
# Clone repository
git clone https://github.com/soh7410/langchain-iointelligence.git
cd langchain-iointelligence

# Install in development mode
pip install -e ".[dev]"

# Setup environment
cp .env.example .env
# Edit .env with your API credentials

# Code formatting & linting
black langchain_iointelligence/ tests/
mypy langchain_iointelligence/
flake8 langchain_iointelligence/

# Run tests
pytest tests/ -v
```

## 📊 Performance & Monitoring

### **Usage Tracking**

```python
chat = IOIntelligenceChat()
response = chat.invoke("Analyze market trends")

# Access detailed usage information
usage = response.usage_metadata
print(f"Prompt tokens: {usage.get('prompt_tokens')}")
print(f"Completion tokens: {usage.get('completion_tokens')}")
print(f"Total tokens: {usage.get('total_tokens')}")
print(f"Model used: {response.response_metadata.get('model')}")
```

### **Response Timing**

```python
import time

start_time = time.time()
response = chat.invoke("Complex reasoning task")
end_time = time.time()

print(f"Response time: {end_time - start_time:.2f} seconds")
print(f"Tokens per second: {response.usage_metadata['total_tokens'] / (end_time - start_time):.1f}")
```

## 🛡️ Production Best Practices

1. **Always use environment variables** for API keys
2. **Implement proper fallback chains** for reliability
3. **Monitor token usage** to control costs
4. **Use streaming** for better user experience
5. **Handle rate limits gracefully** with exponential backoff
6. **Validate models** before deployment

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest tests/ -v`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Create a Pull Request

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/soh7410/langchain-iointelligence/issues)
- **Documentation**: [GitHub Wiki](https://github.com/soh7410/langchain-iointelligence/wiki)
- **Examples**: See `examples/` directory

---

**🎯 Ready for production use with complete ChatGPT API compatibility and modern LangChain integration!**
