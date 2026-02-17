# data_api/main.py

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from agapi.client import AGAPIClient

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Mount static files directory
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

class User(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: str

class UserSearchResponse(BaseModel):
    total: int
    items: List[User]

# Mock database
MOCK_USERS = [
    {
        "id": "u1",
        "name": "Alice Smith",
        "email": "alice@example.com",
        "role": "admin",
        "created_at": "2024-01-01"
    },
    {
        "id": "u2",
        "name": "Bob Johnson",
        "email": "bob@example.com",
        "role": "member",
        "created_at": "2024-01-15"
    },
    {
        "id": "u3",
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "role": "member",
        "created_at": "2024-02-01"
    },
    {
        "id": "u4",
        "name": "Diana Prince",
        "email": "diana@example.com",
        "role": "admin",
        "created_at": "2024-02-10"
    }
]

@app.get("/users/search", response_model=UserSearchResponse)
async def search_users(
    query: Optional[str] = None,
    role: Optional[str] = None,
    limit: int = Query(10, le=100),
    offset: int = 0,
):
    """Search users with optional filtering by name/email and role"""
    filtered_users = MOCK_USERS[:]
    
    # Filter by query (search in name and email)
    if query:
        query_lower = query.lower()
        filtered_users = [
            u for u in filtered_users
            if query_lower in u["name"].lower() or query_lower in u["email"].lower()
        ]
    
    # Filter by role
    if role:
        filtered_users = [u for u in filtered_users if u["role"] == role]
    
    # Apply pagination
    total = len(filtered_users)
    paginated_users = filtered_users[offset:offset + limit]
    
    return {
        "total": total,
        "items": paginated_users
    }

@app.get("/api/")
async def api_root():
    return {"message": "User Data API", "endpoints": ["/users/search", "/api/chat", "/api/status"]}

@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Frontend not found. API available at /api/"}

@app.get("/api/status")
async def get_status():
    """Check system status"""
    gemini_available = bool(os.environ.get("GEMINI_API_KEY"))
    openai_available = bool(os.environ.get("OPENAI_API_KEY"))
    llm_available = gemini_available or openai_available
    
    llm_provider = "Gemini" if gemini_available else ("OpenAI" if openai_available else "None")
    
    return {
        "status": "online",
        "api_version": "1.0",
        "llm_available": llm_available,
        "llm_provider": llm_provider,
        "endpoints": {
            "search": "/users/search",
            "chat": "/api/chat",
            "status": "/api/status"
        }
    }

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Handle chat requests with LLM integration"""
    try:
        # Check if any LLM API key is set
        gemini_key = os.environ.get("GEMINI_API_KEY")
        openai_key = os.environ.get("OPENAI_API_KEY")
        
        if not gemini_key and not openai_key:
            return {
                "error": "LLM API key not configured. Set GEMINI_API_KEY or OPENAI_API_KEY environment variable.",
                "content": "I'm sorry, but I'm not configured with an LLM API key. You can still use the Direct Search tab!",
                "tool_called": False
            }
        
        # Import ChatBackend handler
        from ChatBackend import handle_chat
        
        # Call the chat handler
        response = await handle_chat(request.messages)
        
        return response
        
    except ImportError as e:
        return {
            "error": f"Chat backend not available: {str(e)}",
            "content": "Chat functionality is not available. Please use the Direct Search tab.",
            "tool_called": False
        }
    except Exception as e:
        return {
            "error": str(e),
            "content": f"An error occurred: {str(e)}",
            "tool_called": False
        }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("Starting User Search MCP Demo Server")
    print("="*60)
    print("\n📍 Frontend: http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/docs")
    print("📍 API Root: http://localhost:8000/api/")
    print("\n" + "="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
