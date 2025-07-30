# Unified LLM System

## Overview
Replaced the complex multi-provider LLM module with a single unified `llm.py` containing the `OAI` class that provides OpenAI-compatible interface for all providers.

## Features
- **Single Interface**: One class handles all providers
- **Multiple Providers**: OpenAI, Ollama, Google GenAI, OpenRouter, vLLM
- **Full Feature Support**: 
  - Streaming & non-streaming chat
  - Tool calling with function execution
  - Multimodal support (images, video, audio)
  - Structured outputs (JSON schema, regex, grammar)
- **Auto-configuration**: Provider-specific base URLs and API keys
- **Easy Integration**: Drop-in replacement for existing LLM code

## Configuration

### Default Settings
- **Provider**: Ollama (local)
- **Model**: qwen3:0.6b
- **Base URL**: http://localhost:11434/v1

### Provider Credentials
```python
# Ollama (local) - no credentials needed
# Google GenAI
api_key = "AIzaSyBb8wTvVw9e25aX8XK-eBuu1JzDEPCdqUE"

# OpenRouter  
api_key = "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"

# vLLM (local) - no credentials needed
```

## Usage Examples

### Basic Chat
```python
from llm import OAI

# Use default (Ollama)
llm = OAI(provider="ollama", model="qwen3:0.6b")
response = llm.chat([{"role": "user", "content": "Hello!"}])

# Use Google
llm = OAI(provider="google", api_key="...", model="gemini-2.0-flash-exp")
response = llm.chat(messages)
```

### Streaming
```python
for chunk in llm.stream_chat(messages):
    print(chunk.choices[0].delta.content, end="")
```

### Tool Calling
```python
response = llm.tool_call(messages, tools)
if response.choices[0].message.tool_calls:
    # Execute tools
    llm.execute_tool_calls(response.choices[0].message.tool_calls, available_tools, messages)
```

### Multimodal
```python
response = llm.multimodal_chat(
    text="Describe this image",
    images=["https://example.com/image.jpg"]
)
```

### Convenience Functions
```python
from llm import create_ollama_client, create_google_client

ollama_llm = create_ollama_client(model="qwen3:0.6b")
google_llm = create_google_client(api_key="...", model="gemini-2.0-flash-exp")
```

## Testing
Run the test suite:
```bash
python test_oai_simple.py
```

## Migration
The old `llm/` module has been removed and replaced with:
- Single `llm.py` file with `OAI` class
- Updated `core/input.py` to use new interface
- Updated `core/config.py` with provider configurations

All existing functionality is preserved with improved reliability and performance.