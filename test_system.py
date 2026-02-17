"""
Quick Start Guide for User Search MCP Server

This script demonstrates how to test each component of the system.
"""

import asyncio
import httpx
import sys

async def test_fastapi():
    """Test the FastAPI backend"""
    print("\n" + "="*60)
    print("Testing FastAPI Backend")
    print("="*60)
    
    try:
        async with httpx.AsyncClient() as client:
            # Test root endpoint
            response = await client.get("http://localhost:8000/")
            print(f"✓ Root endpoint: {response.json()}")
            
            # Test search all users
            response = await client.get("http://localhost:8000/users/search")
            data = response.json()
            print(f"✓ All users: Found {data['total']} users")
            
            # Test search with query
            response = await client.get("http://localhost:8000/users/search?query=alice")
            data = response.json()
            print(f"✓ Search 'alice': Found {data['total']} users")
            
            # Test filter by role
            response = await client.get("http://localhost:8000/users/search?role=admin")
            data = response.json()
            print(f"✓ Filter by admin: Found {data['total']} users")
            for user in data['items']:
                print(f"  - {user['name']} ({user['email']})")
            
            print("\n✅ FastAPI Backend is working correctly!")
            return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the FastAPI server is running:")
        print("  python FastAPISample.py")
        return False


async def test_mcp_tool():
    """Test the MCP tool function directly"""
    print("\n" + "="*60)
    print("Testing MCP Tool Function")
    print("="*60)
    
    try:
        from MCPSample import SearchUsersInput, search_users_tool
        
        # Test search for admin users
        input_data = SearchUsersInput(role="admin", limit=5)
        result = await search_users_tool(input_data)
        
        print(f"✓ {result['summary']}")
        print(f"✓ Returned {result['returned']} users:")
        for user in result['users']:
            print(f"  - {user['name']} ({user['role']})")
        
        print("\n✅ MCP Tool is working correctly!")
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the FastAPI server is running first!")
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("User Search MCP Server - System Test")
    print("="*60)
    
    # Test FastAPI
    fastapi_ok = await test_fastapi()
    
    if not fastapi_ok:
        print("\n⚠️  FastAPI server must be running before testing other components.")
        print("\nStart it with: python FastAPISample.py")
        sys.exit(1)
    
    # Test MCP tool
    await test_mcp_tool()
    
    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run the MCP server: python MCPSample.py")
    print("2. Run the chat backend: python ChatBackend.py")
    print("   (Requires OPENAI_API_KEY environment variable)")
    print("\nFor more details, see README.md")


if __name__ == "__main__":
    asyncio.run(main())
