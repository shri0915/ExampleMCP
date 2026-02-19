# chat_backend/handler.py

import json
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from MCPSample import SearchUsersInput, search_users_tool

# Load environment variables from .env file
load_dotenv()

# LLM client will be initialized based on available API key
llm_client = None
llm_provider = None
_initialized = False

def initialize_llm():
    """Initialize LLM client based on available API keys"""
    global llm_client, llm_provider, _initialized
    
    if _initialized and llm_client:
        return True
    
    # Reload .env in case it wasn't loaded yet
    load_dotenv(override=True)
    
    # Try Gemini first
    if os.environ.get("GEMINI_API_KEY"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
            llm_client = genai
            llm_provider = "gemini"
            _initialized = True
            print("✓ Using Google Gemini")
            return True
        except ImportError:
            print("⚠️  google-generativeai not installed. Install with: pip install google-generativeai")
    
    # Try OpenAI
    if os.environ.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            llm_client = OpenAI()
            llm_provider = "openai"
            _initialized = True
            print("✓ Using OpenAI")
            return True
        except ImportError:
            print("⚠️  openai not installed. Install with: pip install openai")
    
    return False

# Initialize on module load
initialize_llm()

# Tool schema for the LLM
search_users_schema = {
    "type": "function",
    "function": {
        "name": "search_users",
        "description": "Search for users by name, email, or role. Available roles: admin, member, developer, PM",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Free text search across name and email"
                },
                "role": {
                    "type": "string",
                    "description": "Filter by role. Valid values: admin, member, developer, PM"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                },
                "offset": {
                    "type": "integer",
                    "description": "Pagination offset",
                    "default": 0
                }
            }
        }
    }
}


async def handle_chat(messages: List[Dict[str, str]], model: Optional[str] = None) -> Dict[str, Any]:
    """
    Handle chat messages with tool calling support.
    
    Args:
        messages: List of chat messages with 'role' and 'content'
        model: Model to use (auto-selected if None)
        
    Returns:
        Response from the LLM
    """
    # Ensure LLM is initialized (in case .env was loaded after module import)
    if not llm_client:
        initialize_llm()
    
    if not llm_client:
        raise ValueError("No LLM configured. Set GEMINI_API_KEY or OPENAI_API_KEY environment variable.")
    
    if llm_provider == "gemini":
        return await handle_chat_gemini(messages, model or "gemini-2.5-flash")
    else:
        return await handle_chat_openai(messages, model or "gpt-4o-mini")


async def handle_chat_openai(messages: List[Dict[str, str]], model: str) -> Dict[str, Any]:
    """Handle chat with OpenAI"""
    # First call to LLM with tools available
    response = llm_client.chat.completions.create(
        model=model,
        messages=messages,
        tools=[search_users_schema],
        tool_choice="auto"
    )

    message = response.choices[0].message
    
    # Check if the model wants to call a tool
    if message.tool_calls:
        # Add assistant's message to conversation
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
        })
        
        # Execute each tool call
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            if tool_name == "search_users":
                # Call the actual tool
                result = await search_users_tool(
                    SearchUsersInput(**tool_args)
                )
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result)
                })
        
        # Make second call to LLM with tool results
        final_response = llm_client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        return {
            "content": final_response.choices[0].message.content,
            "role": "assistant",
            "tool_called": True,
            "finish_reason": final_response.choices[0].finish_reason
        }
    
    # No tool calls, return the response directly
    return {
        "content": message.content,
        "role": "assistant",
        "tool_called": False,
        "finish_reason": response.choices[0].finish_reason
    }


async def handle_chat_gemini(messages: List[Dict[str, str]], model: str) -> Dict[str, Any]:
    """Handle chat with Google Gemini"""
    try:
        # Convert messages to Gemini format
        gemini_messages = []
        system_instruction = None
        
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            elif msg["role"] == "user":
                gemini_messages.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                gemini_messages.append({"role": "model", "parts": [msg["content"]]})
        
        # Define tool for Gemini
        search_tool = llm_client.protos.Tool(
            function_declarations=[
                llm_client.protos.FunctionDeclaration(
                    name="search_users",
                    description="Search for users by name, email, or role. Available roles: admin, member, developer, PM",
                    parameters=llm_client.protos.Schema(
                        type=llm_client.protos.Type.OBJECT,
                        properties={
                            "query": llm_client.protos.Schema(
                                type=llm_client.protos.Type.STRING,
                                description="Free text search across name and email"
                            ),
                            "role": llm_client.protos.Schema(
                                type=llm_client.protos.Type.STRING,
                                description="Filter by role. Valid values: admin, member, developer, PM"
                            ),
                            "limit": llm_client.protos.Schema(
                                type=llm_client.protos.Type.INTEGER,
                                description="Maximum number of results to return"
                            ),
                        }
                    )
                )
            ]
        )
        
        # Create model with tools
        gemini_model = llm_client.GenerativeModel(
            model_name=model,
            tools=[search_tool],
            system_instruction=system_instruction
        )
        
        # Start chat
        chat = gemini_model.start_chat(history=gemini_messages[:-1] if len(gemini_messages) > 1 else [])
        
        # Send the last message
        last_message = gemini_messages[-1]["parts"][0] if gemini_messages else ""
        response = chat.send_message(last_message)
        
        # Check for function calls
        function_call = None
        try:
            if response.candidates and response.candidates[0].content.parts:
                first_part = response.candidates[0].content.parts[0]
                if hasattr(first_part, 'function_call') and first_part.function_call:
                    function_call = first_part.function_call
        except (AttributeError, IndexError):
            pass
        
        if function_call:
            tool_name = function_call.name
            tool_args = dict(function_call.args)
            
            # Execute the tool
            if tool_name == "search_users":
                result = await search_users_tool(SearchUsersInput(**tool_args))
                
                # Send result back to model
                response = chat.send_message(
                    llm_client.protos.Content(
                        parts=[llm_client.protos.Part(
                            function_response=llm_client.protos.FunctionResponse(
                                name=tool_name,
                                response={"result": result}
                            )
                        )]
                    )
                )
                
                # Extract text from the response after tool execution
                response_text = response.text if hasattr(response, 'text') else str(response)
                
                return {
                    "content": response_text,
                    "role": "assistant",
                    "tool_called": True,
                    "finish_reason": "stop"
                }
        
        # No tool call - extract text safely
        response_text = response.text if hasattr(response, 'text') else "I apologize, but I couldn't generate a proper response."
        
        return {
            "content": response_text,
            "role": "assistant",
            "tool_called": False,
            "finish_reason": "stop"
        }
    
    except Exception as e:
        error_msg = str(e)
        print(f"Error in Gemini chat handler: {error_msg}")
        return {
            "content": f"I encountered an error while processing your request: {error_msg}. Please try rephrasing your question.",
            "role": "assistant",
            "tool_called": False,
            "finish_reason": "error"
        }


async def main():
    """Example usage of the chat handler"""
    print("Chat Backend Example")
    print("=" * 50)
    print(f"Using: {llm_provider or 'No LLM configured'}")
    print("=" * 50)
    
    # Example conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can search for users in our database."},
        {"role": "user", "content": "Can you find all admin users?"}
    ]
    
    print("\nUser: Can you find all admin users?")
    response = await handle_chat(messages)
    
    print(f"\nAssistant: {response['content']}")
    print(f"\nTool called: {response['tool_called']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
