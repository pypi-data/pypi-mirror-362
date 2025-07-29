# QV Ollama SDK

A simple SDK for interacting with the Ollama API with **thinking mode** and **tool calling** support.

## Features

- 🧠 **Thinking Mode** - See AI reasoning process before answers
- 🛠️ **Tool Calling** - Execute Python functions automatically  
- 💬 **Simple Conversation** - Easy chat interface
- ⚡ **Streaming Support** - Real-time responses
- 🔧 **Explicit Parameters** - No unnecessary defaults
- 🛡️ **Model Compatibility** - Auto-fallback for unsupported features

## Installation

```bash
pip install qv-ollama-sdk
```

## Quick Start

```python
from qv_ollama_sdk import OllamaChatClient

# Create a client with a system message
client = OllamaChatClient(
    model_name="qwen3:8b",
    system_message="You are a helpful assistant."
)

# Simple chat - uses Ollama's default parameters
response = client.chat("What is the capital of France?")
print(response.content)

# Continue the conversation
response = client.chat("And what is its population?")
print(response.content)

# Set specific parameters only when you need them
client.temperature = 1.0  # Using property setter
client.max_tokens = 500   # Using property setter
client.set_parameters(num_ctx=2048)  # For multiple parameters

# Get conversation history
history = client.get_history()
```

## 🧠 Thinking Mode

```python
# Enable thinking globally
client.enable_thinking()
response = client.chat("Solve this complex problem...")
print(f"🧠 Thinking: {response.thinking}")
print(f"💬 Answer: {response.content}")

# Disable when you want fast responses
client.disable_thinking()
```

## 🛠️ Tool Calling

```python
def add_numbers(a: str, b: str) -> str:
    """Add two numbers."""
    return str(int(a) + int(b))

def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Sunny in {city}, 23°C"

tools = [add_numbers, get_weather]

# AI automatically calls functions when needed
response = client.chat("What's 15+27? And weather in Berlin?", tools=tools)
print(response.content)
```

## 🎯 Thinking + Tools

```python
client.enable_thinking()
response = client.chat("Calculate 25 + 18", tools=tools)

print(f"🧠 Thinking: {response.thinking}")
print(f"💬 Answer: {response.content}")
print(f"🛠️ Tools used: {len(response.tool_calls)}")
```

## ⚡ Streaming

```python
# Stream with thinking and tools
for chunk in client.stream_chat("Add 12 + 8", tools=tools):
    if chunk.thinking:
        print(chunk.thinking, end="")
    if chunk.tool_calls:
        print(f"🛠️ Using: {chunk.tool_calls[0].function.name}")
    if chunk.content:
        print(chunk.content, end="")
```

## API Reference

### Main Methods
- `chat(message, tools=None, auto_execute=True)` - Get response
- `stream_chat(message, tools=None, auto_execute=True)` - Stream response

### Thinking Control
- `enable_thinking()` - Enable thinking globally
- `disable_thinking()` - Disable thinking globally

### Response Object
- `response.content` - The answer
- `response.thinking` - AI's thought process
- `response.tool_calls` - Tools that were called
- `response.tool_results` - Tool execution results

### Parameters
- `tools=None` - List of Python functions
- `auto_execute=True` - Auto-run tools (default)
- `auto_execute=False` - Raw tool calls only

## 🛡️ Model Compatibility

The SDK automatically handles different model capabilities:

```python
# Works with any model - features auto-disabled if unsupported
client = OllamaChatClient(model_name="gemma2:2b")  # No tool/thinking support
client.enable_thinking()  # Will be ignored if not supported
tools = [add_numbers]

# This still works! Falls back to normal chat
response = client.chat("What is 15 + 27?", tools=tools)
# → "15 + 27 equals 42" (calculated by model, no tools used)
```

**Supported Models:**
- ✅ **Modern models** (e.g., `qwen3:8b`) - Full features
- ✅ **Tool-only models** (e.g., `llama3:8b`) - Tools but no thinking  
- ✅ **Thinking-only models** - Thinking but no tools
- ✅ **Basic models** (e.g., `gemma2:2b`) - Normal chat only

**Graceful Degradation:**
- Unsupported features are automatically disabled
- No errors or exceptions thrown
- Always provides a response

## Advanced Usage

For more control, you can use the lower-level API:

```python
from qv_ollama_sdk import Conversation, OllamaConversationService, ModelParameters

# Create a conversation
conversation = Conversation(model_name="qwen3:8b")
conversation.add_system_message("You are a helpful assistant.")
conversation.add_user_message("What is the capital of France?")

# Generate a response with specific parameters including thinking
service = OllamaConversationService()
parameters = ModelParameters(temperature=0.7, num_ctx=2048, think=True)
response = service.generate_response(conversation, parameters)

print(f"Thinking: {response.thinking}")
print(f"Answer: {response.content}")
```
