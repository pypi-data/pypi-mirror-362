# MBX AI

A Python library for building AI applications with LLMs.

## Features

- **OpenRouter Integration**: Connect to various LLM providers through OpenRouter
- **Tool Integration**: Easily integrate tools with LLMs using the Model Context Protocol (MCP)
- **Structured Output**: Get structured, typed responses from LLMs
- **Chat Interface**: Simple chat interface for interacting with LLMs
- **FastAPI Server**: Built-in FastAPI server for tool integration

## Installation

```bash
pip install mbxai
```

## Quick Start

### Basic Usage

```python
from mbxai import OpenRouterClient

# Initialize the client
client = OpenRouterClient(api_key="your-api-key")

# Chat with an LLM
response = await client.chat([
    {"role": "user", "content": "Hello, how are you?"}
])
print(response.choices[0].message.content)
```

### Using Tools

```python
from mbxai import OpenRouterClient, ToolClient
from pydantic import BaseModel

# Define your tool's input and output models
class CalculatorInput(BaseModel):
    a: float
    b: float

class CalculatorOutput(BaseModel):
    result: float

# Create a calculator tool
async def calculator(input: CalculatorInput) -> CalculatorOutput:
    return CalculatorOutput(result=input.a + input.b)

# Initialize the client with tools
client = ToolClient(OpenRouterClient(api_key="your-api-key"))
client.add_tool(calculator)

# Use the tool in a chat
response = await client.chat([
    {"role": "user", "content": "What is 2 + 3?"}
])
print(response.choices[0].message.content)
```

### Using MCP (Model Context Protocol)

```python
from mbxai import OpenRouterClient, MCPClient
from mbxai.mcp import MCPServer
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

# Define your tool's input and output models
class CalculatorInput(BaseModel):
    a: float
    b: float

class CalculatorOutput(BaseModel):
    result: float

# Create a FastMCP instance
mcp = FastMCP("calculator-service")

# Create a calculator tool
@mcp.tool()
async def calculator(argument: CalculatorInput) -> CalculatorOutput:
    return CalculatorOutput(result=argument.a + argument.b)

# Start the MCP server
server = MCPServer("calculator-service")
await server.add_tool(calculator)
await server.start()

# Initialize the MCP client
client = MCPClient(OpenRouterClient(api_key="your-api-key"))
await client.register_mcp_server("calculator-service", "http://localhost:8000")

# Use the tool in a chat
response = await client.chat([
    {"role": "user", "content": "What is 2 + 3?"}
])
print(response.choices[0].message.content)
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mbxai.git
cd mbxai
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

## License

MIT License