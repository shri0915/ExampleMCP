# User Search MCP Server

This project demonstrates a Model Context Protocol (MCP) server with a FastAPI backend, LLM chat integration, and a web-based frontend.

## Project Structure

```
ExampleMCP/
├── FastAPISample.py      # FastAPI backend with user search API
├── MCPSample.py          # MCP server implementation
├── ChatBackend.py        # LLM chat handler with tool calling
├── static/
│   └── index.html        # Web frontend UI
├── launcher.py           # Easy launcher script
├── test_system.py        # System tests
├── test_frontend.py      # Frontend tests
├── toolDefinition.json   # Tool schema definition
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Features

- **Web Frontend**: Beautiful, responsive UI with chat and search interfaces
- **FastAPI Backend**: REST API for searching users with filtering and pagination
- **MCP Server**: Model Context Protocol server exposing user search as a tool
- **LLM Integration**: Chat handler with OpenAI integration and tool calling support
- **Mock Database**: Sample user data for testing

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python FastAPISample.py
```

### 3. Open the Frontend

Open your browser and go to: **http://localhost:8000**

You'll see three tabs:
- **💬 AI Chat**: Natural language chat with LLM (requires OpenAI API key)
- **🔍 Direct Search**: Direct API search (works without API key)
- **ℹ️ About**: Information about the demo

### 4. (Optional) Enable AI Chat

To use the AI Chat feature, set your OpenAI API key:

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"

# Windows (CMD)
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY=your-api-key-here
```

Then restart the server.

## API Endpoints

### GET /users/search

Search for users with optional filtering.

**Query Parameters:**
- `query` (optional): Search text for name or email
- `role` (optional): Filter by role (admin, member, etc.)
- `limit` (optional): Maximum results (default: 10, max: 100)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "total": 4,
  "items": [
    {
      "id": "u1",
      "name": "Alice Smith",
      "email": "alice@example.com",
      "role": "admin",
      "created_at": "2024-01-01"
    }
  ]
}
```

## MCP Tool

### search_users

Search for users by name, email, or role.

**Parameters:**
- `query` (string, optional): Free text search
- `role` (string, optional): Filter by role
- `limit` (integer, optional): Max results (≤100)
- `offset` (integer, optional): Pagination offset

**Returns:**
```json
{
  "summary": "Found 2 users",
  "total": 2,
  "returned": 2,
  "users": [...]
}
```

## Example Usage

### Using the Chat Backend

```python
import asyncio
from ChatBackend import handle_chat

async def main():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Find all admin users"}
    ]
    
    response = await handle_chat(messages)
    print(response['content'])

asyncio.run(main())
```

## Development

### Adding More Users

Edit the `MOCK_USERS` list in [FastAPISample.py](FastAPISample.py) to add more sample data.

### Customizing the MCP Server

Modify [MCPSample.py](MCPSample.py) to add new tools or change the behavior of existing ones.

### Using Different LLM Providers

The chat backend uses OpenAI by default, but you can modify [ChatBackend.py](ChatBackend.py) to use:
- Anthropic Claude
- Groq
- Azure OpenAI
- Any OpenAI-compatible API

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, change it in both files:
- [FastAPISample.py](FastAPISample.py): `uvicorn.run(app, host="0.0.0.0", port=8000)`
- [MCPSample.py](MCPSample.py): `DATA_API_URL = "http://localhost:8000"`

### Connection Refused

Make sure the FastAPI backend is running before starting the MCP server or chat backend.

### OpenAI API Errors

Ensure your `OPENAI_API_KEY` environment variable is set correctly.

## License

This is a sample project for demonstration purposes.
