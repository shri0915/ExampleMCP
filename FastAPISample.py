# data_api/main.py

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

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
    {"id": "u1", "name": "Alice Smith", "email": "alice@example.com", "role": "admin", "created_at": "2024-01-01"},
    {"id": "u2", "name": "Bob Johnson", "email": "bob@example.com", "role": "developer", "created_at": "2024-01-15"},
    {"id": "u3", "name": "Charlie Brown", "email": "charlie@example.com", "role": "PM", "created_at": "2024-02-01"},
    {"id": "u4", "name": "Diana Prince", "email": "diana@example.com", "role": "admin", "created_at": "2024-02-10"},
    {"id": "u5", "name": "Eve Martinez", "email": "eve@example.com", "role": "developer", "created_at": "2024-02-15"},
    {"id": "u6", "name": "Frank Wilson", "email": "frank@example.com", "role": "PM", "created_at": "2024-02-20"},
    {"id": "u7", "name": "Grace Lee", "email": "grace@example.com", "role": "admin", "created_at": "2024-03-01"},
    {"id": "u8", "name": "Henry Davis", "email": "henry@example.com", "role": "developer", "created_at": "2024-03-05"},
    {"id": "u9", "name": "Ivy Chen", "email": "ivy@example.com", "role": "developer", "created_at": "2024-03-10"},
    {"id": "u10", "name": "Jack Thompson", "email": "jack@example.com", "role": "PM", "created_at": "2024-03-15"},
    {"id": "u11", "name": "Kate Anderson", "email": "kate@example.com", "role": "admin", "created_at": "2024-03-20"},
    {"id": "u12", "name": "Liam Garcia", "email": "liam@example.com", "role": "developer", "created_at": "2024-03-25"},
    {"id": "u13", "name": "Maya Patel", "email": "maya@example.com", "role": "developer", "created_at": "2024-04-01"},
    {"id": "u14", "name": "Noah Kim", "email": "noah@example.com", "role": "PM", "created_at": "2024-04-05"},
    {"id": "u15", "name": "Olivia Rodriguez", "email": "olivia@example.com", "role": "admin", "created_at": "2024-04-10"},
    {"id": "u16", "name": "Peter White", "email": "peter@example.com", "role": "developer", "created_at": "2024-04-15"},
    {"id": "u17", "name": "Quinn Taylor", "email": "quinn@example.com", "role": "developer", "created_at": "2024-04-20"},
    {"id": "u18", "name": "Rachel Green", "email": "rachel@example.com", "role": "PM", "created_at": "2024-04-25"},
    {"id": "u19", "name": "Sam Cooper", "email": "sam@example.com", "role": "admin", "created_at": "2024-05-01"},
    {"id": "u20", "name": "Tina Brooks", "email": "tina@example.com", "role": "developer", "created_at": "2024-05-05"},
    {"id": "u21", "name": "Uma Singh", "email": "uma@example.com", "role": "developer", "created_at": "2024-05-10"},
    {"id": "u22", "name": "Victor Stone", "email": "victor@example.com", "role": "PM", "created_at": "2024-05-15"},
    {"id": "u23", "name": "Wendy Clark", "email": "wendy@example.com", "role": "admin", "created_at": "2024-05-20"},
    {"id": "u24", "name": "Xavier Lopez", "email": "xavier@example.com", "role": "developer", "created_at": "2024-05-25"},
    {"id": "u25", "name": "Yara Ahmed", "email": "yara@example.com", "role": "developer", "created_at": "2024-06-01"},
    {"id": "u26", "name": "Zack Morris", "email": "zack@example.com", "role": "PM", "created_at": "2024-06-05"},
    {"id": "u27", "name": "Amy Wong", "email": "amy@example.com", "role": "admin", "created_at": "2024-06-10"},
    {"id": "u28", "name": "Ben Parker", "email": "ben@example.com", "role": "developer", "created_at": "2024-06-15"},
    {"id": "u29", "name": "Chloe Bennett", "email": "chloe@example.com", "role": "developer", "created_at": "2024-06-20"},
    {"id": "u30", "name": "David Miller", "email": "david@example.com", "role": "PM", "created_at": "2024-06-25"},
    {"id": "u31", "name": "Emma Watson", "email": "emma@example.com", "role": "admin", "created_at": "2024-07-01"},
    {"id": "u32", "name": "Felix Harper", "email": "felix@example.com", "role": "developer", "created_at": "2024-07-05"},
    {"id": "u33", "name": "Gina Torres", "email": "gina@example.com", "role": "developer", "created_at": "2024-07-10"},
    {"id": "u34", "name": "Harry Potter", "email": "harry@example.com", "role": "PM", "created_at": "2024-07-15"},
    {"id": "u35", "name": "Iris West", "email": "iris@example.com", "role": "admin", "created_at": "2024-07-20"},
    {"id": "u36", "name": "James Bond", "email": "james@example.com", "role": "developer", "created_at": "2024-07-25"},
    {"id": "u37", "name": "Kelly Kapoor", "email": "kelly@example.com", "role": "developer", "created_at": "2024-08-01"},
    {"id": "u38", "name": "Leo Valdez", "email": "leo@example.com", "role": "PM", "created_at": "2024-08-05"},
    {"id": "u39", "name": "Mia Wallace", "email": "mia@example.com", "role": "admin", "created_at": "2024-08-10"},
    {"id": "u40", "name": "Nick Fury", "email": "nick@example.com", "role": "developer", "created_at": "2024-08-15"},
    {"id": "u41", "name": "Oscar Martinez", "email": "oscar@example.com", "role": "developer", "created_at": "2024-08-20"},
    {"id": "u42", "name": "Pam Beesly", "email": "pam@example.com", "role": "PM", "created_at": "2024-08-25"},
    {"id": "u43", "name": "Quentin Beck", "email": "quentin@example.com", "role": "admin", "created_at": "2024-09-01"},
    {"id": "u44", "name": "Rosa Diaz", "email": "rosa@example.com", "role": "developer", "created_at": "2024-09-05"},
    {"id": "u45", "name": "Steve Rogers", "email": "steve@example.com", "role": "developer", "created_at": "2024-09-10"},
    {"id": "u46", "name": "Tony Stark", "email": "tony@example.com", "role": "PM", "created_at": "2024-09-15"},
    {"id": "u47", "name": "Ursula Vernon", "email": "ursula@example.com", "role": "admin", "created_at": "2024-09-20"},
    {"id": "u48", "name": "Vince Gilligan", "email": "vince@example.com", "role": "developer", "created_at": "2024-09-25"},
    {"id": "u49", "name": "Wanda Maximoff", "email": "wanda@example.com", "role": "developer", "created_at": "2024-10-01"},
    {"id": "u50", "name": "Xander Harris", "email": "xander@example.com", "role": "PM", "created_at": "2024-10-05"},
    {"id": "u51", "name": "Yelena Belova", "email": "yelena@example.com", "role": "admin", "created_at": "2024-10-10"},
    {"id": "u52", "name": "Zachary Levi", "email": "zachary@example.com", "role": "developer", "created_at": "2024-10-15"},
    {"id": "u53", "name": "Anna Kendrick", "email": "anna@example.com", "role": "developer", "created_at": "2024-10-20"},
    {"id": "u54", "name": "Bruce Wayne", "email": "bruce@example.com", "role": "PM", "created_at": "2024-10-25"},
    {"id": "u55", "name": "Carol Danvers", "email": "carol@example.com", "role": "admin", "created_at": "2024-11-01"},
    {"id": "u56", "name": "Derek Hale", "email": "derek@example.com", "role": "developer", "created_at": "2024-11-05"},
    {"id": "u57", "name": "Elena Gilbert", "email": "elena@example.com", "role": "developer", "created_at": "2024-11-10"},
    {"id": "u58", "name": "Finn Hudson", "email": "finn@example.com", "role": "PM", "created_at": "2024-11-15"},
    {"id": "u59", "name": "Gwen Stacy", "email": "gwen@example.com", "role": "admin", "created_at": "2024-11-20"},
    {"id": "u60", "name": "Hank Pym", "email": "hank@example.com", "role": "developer", "created_at": "2024-11-25"},
    {"id": "u61", "name": "Isabelle Lightwood", "email": "isabelle@example.com", "role": "developer", "created_at": "2024-12-01"},
    {"id": "u62", "name": "Jake Peralta", "email": "jake@example.com", "role": "PM", "created_at": "2024-12-05"},
    {"id": "u63", "name": "Kara Danvers", "email": "kara@example.com", "role": "admin", "created_at": "2024-12-10"},
    {"id": "u64", "name": "Luke Skywalker", "email": "luke@example.com", "role": "developer", "created_at": "2024-12-15"},
    {"id": "u65", "name": "Monica Geller", "email": "monica@example.com", "role": "developer", "created_at": "2024-12-20"},
    {"id": "u66", "name": "Natasha Romanoff", "email": "natasha@example.com", "role": "PM", "created_at": "2024-12-25"},
    {"id": "u67", "name": "Oliver Queen", "email": "oliver@example.com", "role": "admin", "created_at": "2025-01-01"},
    {"id": "u68", "name": "Piper Halliwell", "email": "piper@example.com", "role": "developer", "created_at": "2025-01-05"},
    {"id": "u69", "name": "Quicksilver Pietro", "email": "pietro@example.com", "role": "developer", "created_at": "2025-01-10"},
    {"id": "u70", "name": "Raven Darkholme", "email": "raven@example.com", "role": "PM", "created_at": "2025-01-15"},
    {"id": "u71", "name": "Scott Lang", "email": "scott@example.com", "role": "admin", "created_at": "2025-01-20"},
    {"id": "u72", "name": "Thea Queen", "email": "thea@example.com", "role": "developer", "created_at": "2025-01-25"},
    {"id": "u73", "name": "Uther Pendragon", "email": "uther@example.com", "role": "developer", "created_at": "2025-02-01"},
    {"id": "u74", "name": "Violet Parr", "email": "violet@example.com", "role": "PM", "created_at": "2025-02-05"},
    {"id": "u75", "name": "Wade Wilson", "email": "wade@example.com", "role": "admin", "created_at": "2025-02-10"},
    {"id": "u76", "name": "Xavier Institute", "email": "xavier.inst@example.com", "role": "developer", "created_at": "2025-02-15"},
    {"id": "u77", "name": "Ygritte Snow", "email": "ygritte@example.com", "role": "developer", "created_at": "2025-02-20"},
    {"id": "u78", "name": "Zoe Washburne", "email": "zoe@example.com", "role": "PM", "created_at": "2025-02-25"},
    {"id": "u79", "name": "Arthur Curry", "email": "arthur@example.com", "role": "admin", "created_at": "2025-03-01"},
    {"id": "u80", "name": "Barbara Gordon", "email": "barbara@example.com", "role": "developer", "created_at": "2025-03-05"},
    {"id": "u81", "name": "Clint Barton", "email": "clint@example.com", "role": "developer", "created_at": "2025-03-10"},
    {"id": "u82", "name": "Donna Troy", "email": "donna@example.com", "role": "PM", "created_at": "2025-03-15"},
    {"id": "u83", "name": "Erik Lehnsherr", "email": "erik@example.com", "role": "admin", "created_at": "2025-03-20"},
    {"id": "u84", "name": "Felicity Smoak", "email": "felicity@example.com", "role": "developer", "created_at": "2025-03-25"},
    {"id": "u85", "name": "Garfield Logan", "email": "garfield@example.com", "role": "developer", "created_at": "2025-04-01"},
    {"id": "u86", "name": "Harley Quinn", "email": "harley@example.com", "role": "PM", "created_at": "2025-04-05"},
    {"id": "u87", "name": "Irie Shouichi", "email": "irie@example.com", "role": "admin", "created_at": "2025-04-10"},
    {"id": "u88", "name": "Jessica Jones", "email": "jessica@example.com", "role": "developer", "created_at": "2025-04-15"},
    {"id": "u89", "name": "Kitty Pryde", "email": "kitty@example.com", "role": "developer", "created_at": "2025-04-20"},
    {"id": "u90", "name": "Lois Lane", "email": "lois@example.com", "role": "PM", "created_at": "2025-04-25"},
    {"id": "u91", "name": "Matt Murdock", "email": "matt@example.com", "role": "admin", "created_at": "2025-05-01"},
    {"id": "u92", "name": "Nora Allen", "email": "nora@example.com", "role": "developer", "created_at": "2025-05-05"},
    {"id": "u93", "name": "Ororo Munroe", "email": "ororo@example.com", "role": "developer", "created_at": "2025-05-10"},
    {"id": "u94", "name": "Peggy Carter", "email": "peggy@example.com", "role": "PM", "created_at": "2025-05-15"},
    {"id": "u95", "name": "Queenie Goldstein", "email": "queenie@example.com", "role": "admin", "created_at": "2025-05-20"},
    {"id": "u96", "name": "Roy Harper", "email": "roy@example.com", "role": "developer", "created_at": "2025-05-25"},
    {"id": "u97", "name": "Selina Kyle", "email": "selina@example.com", "role": "developer", "created_at": "2025-06-01"},
    {"id": "u98", "name": "Thor Odinson", "email": "thor@example.com", "role": "PM", "created_at": "2025-06-05"},
    {"id": "u99", "name": "Ukitake Jushiro", "email": "ukitake@example.com", "role": "admin", "created_at": "2025-06-10"},
    {"id": "u100", "name": "Vision Synthezoid", "email": "vision@example.com", "role": "developer", "created_at": "2025-06-15"}
]

@app.get("/users/search", response_model=UserSearchResponse)
async def search_users(
    query: Optional[str] = None,
    role: Optional[str] = None,
    limit: int = Query(10),
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
