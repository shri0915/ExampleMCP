# mcp_adapter/server.py

from typing import Optional
from pydantic import BaseModel, Field
import httpx
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

DATA_API_URL = "http://localhost:8000"

# Tool input schema
class SearchUsersInput(BaseModel):
    query: Optional[str] = Field(
        None,
        description="Free text search across name and email"
    )
    role: Optional[str] = Field(
        None,
        description="Filter users by role (admin, member, etc.)"
    )
    limit: int = Field(
        10,
        description="Maximum number of users to return (max 100)",
        le=100
    )
    offset: int = Field(
        0,
        description="Pagination offset"
    )


async def search_users_tool(input: SearchUsersInput):
    """Call the data API to search for users"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DATA_API_URL}/users/search",
            params=input.model_dump(exclude_none=True),
        )

    response.raise_for_status()
    data = response.json()

    # 🔥 IMPORTANT: Keep tool responses structured + safe
    return {
        "summary": f"Found {data['total']} users",
        "total": data["total"],
        "returned": len(data["items"]),
        "users": data["items"],
    }


# Create MCP server instance
app = Server("user-search-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="search_users",
            description="Search for users by name, email, or role.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Free text search across name and email"
                    },
                    "role": {
                        "type": "string",
                        "description": "Filter by role (e.g., admin, member)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (<=100)",
                        "default": 10
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Pagination offset",
                        "default": 0
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    if name == "search_users":
        try:
            # Validate and parse input
            input_data = SearchUsersInput(**arguments)
            
            # Call the tool function
            result = await search_users_tool(input_data)
            
            # Format response for MCP
            import json
            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
