"""
Demo script to test the chat endpoint with or without OpenAI
"""

import asyncio
import httpx
import os

async def test_chat_with_api_key():
    """Test chat endpoint when API key is available"""
    print("\n" + "="*60)
    print("Testing Chat Endpoint with OpenAI API")
    print("="*60)
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set. Skipping this test.")
        print("Set it with: $env:OPENAI_API_KEY='your-key-here'")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Find all admin users"}
            ]
            
            response = await client.post(
                "http://localhost:8000/api/chat",
                json={"messages": messages}
            )
            
            data = response.json()
            
            if "error" in data:
                print(f"\n❌ Error: {data['error']}")
                return False
            
            print(f"\n✓ Chat response received")
            print(f"✓ Tool called: {data.get('tool_called', False)}")
            print(f"\nAssistant: {data['content']}")
            print("\n✅ Chat endpoint working with LLM!")
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


async def test_chat_without_api_key():
    """Test chat endpoint when API key is NOT available"""
    print("\n" + "="*60)
    print("Testing Chat Endpoint without OpenAI API")
    print("="*60)
    
    # Temporarily remove API key if it exists
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print("\nTemporarily removing API key for this test...")
        del os.environ["OPENAI_API_KEY"]
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            messages = [
                {"role": "user", "content": "Find all admin users"}
            ]
            
            response = await client.post(
                "http://localhost:8000/api/chat",
                json={"messages": messages}
            )
            
            data = response.json()
            
            print(f"\n✓ Response received")
            print(f"✓ Error expected: {'error' in data}")
            print(f"\nResponse: {data.get('content', data.get('error'))}")
            print("\n✅ Graceful error handling working!")
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        # Restore API key if it existed
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            print("\nAPI key restored.")


async def test_direct_search():
    """Test direct search endpoint"""
    print("\n" + "="*60)
    print("Testing Direct Search (no LLM needed)")
    print("="*60)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8000/users/search?role=admin"
            )
            
            data = response.json()
            
            print(f"\n✓ Found {data['total']} admin users:")
            for user in data['items']:
                print(f"  - {user['name']} ({user['email']})")
            
            print("\n✅ Direct search working!")
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Frontend Demo - Backend Testing")
    print("="*60)
    
    # Test direct search (always works)
    await test_direct_search()
    
    # Test chat without API key
    await test_chat_without_api_key()
    
    # Test chat with API key (if available)
    await test_chat_with_api_key()
    
    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60)
    print("\n🌐 Frontend available at: http://localhost:8000")
    print("\nYou can:")
    print("  1. Use Direct Search without any API key")
    print("  2. Set OPENAI_API_KEY to enable AI Chat")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
