# Demiurg

A flexible AI agent framework for building intelligent agents with support for multiple LLM providers.

## Features

- 🚀 Simple, minimal API for quick agent creation
- 🔌 Support for multiple LLM providers (OpenAI, Anthropic, Google, etc.)
- 📬 Built-in messaging system with conversation history
- 📁 File handling capabilities (images, audio, text)
- 🔧 Extensible tool system with Composio integration
- 🏗️ Production-ready with built-in queue management
- 🐳 Designed for both cloud and local container deployment

## Installation

```bash
pip install demiurg
```

## Quick Start

```python
from demiurg import Agent

# Create an agent with default configuration
agent = Agent()

# Or customize your agent
agent = Agent(
    name="My Custom Agent",
    model="gpt-4",
    temperature=0.7,
    provider="openai"
)
```

## Basic Usage

### Sending Messages

```python
from demiurg import send_text, send_file

# Send a text message
await send_text(conversation_id, "Hello from my agent!")

# Send a file
await send_file(conversation_id, "/path/to/file.png", caption="Check this out!")
```

### Getting Conversation History

```python
from demiurg import get_conversation_history

# Get formatted conversation history
messages = await get_conversation_history(
    conversation_id,
    limit=50,
    provider="openai"  # Format for specific LLM provider
)
```

### Custom Agent Implementation

```python
from demiurg import Agent

class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Helpful Assistant",
            model="gpt-4",
            system_prompt="You are a helpful AI assistant."
        )
    
    async def process_message(self, message, provider="openai"):
        # Add custom logic here
        response = await super().process_message(message, provider)
        return response

agent = MyAgent()
```

## Environment Variables

The framework uses environment variables for configuration:

- `DEMIURG_BACKEND_URL`: Backend API URL (default: `http://backend:3000`)
- `DEMIURG_AGENT_TOKEN`: Authentication token
- `DEMIURG_AGENT_ID`: Unique agent identifier
- `OPENAI_API_KEY`: OpenAI API key (for OpenAI provider)
- `COMPOSIO_API_KEY`: Composio API key (for tool integration)

## Provider Support

Currently supported:
- ✅ OpenAI (GPT-3.5, GPT-4, etc.)

Coming soon:
- 🚧 Anthropic (Claude)
- 🚧 Google (Gemini)
- 🚧 Cohere
- 🚧 Local models

## Development

For development access and contribution guidelines, please contact support@demiurg.ai.

## License

Copyright © 2024 Demiurg AI. All rights reserved.

This is proprietary software. See LICENSE file for details.