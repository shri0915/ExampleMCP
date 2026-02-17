"""
Launcher script for the User Search MCP Server project

Usage:
    python launcher.py [component]

Components:
    frontend - Start the server with web frontend (recommended)
    api      - Start the FastAPI backend server only
    mcp      - Start the MCP server (requires API to be running)
    chat     - Run the chat backend example (requires API and OPENAI_API_KEY)
    test     - Run system tests
    all      - Show instructions to run all components
"""

import sys
import subprocess
import os

def check_api_running():
    """Check if the FastAPI server is running"""
    import httpx
    try:
        response = httpx.get("http://localhost:8000/", timeout=2)
        return response.status_code == 200
    except:
        return False


def launch_api():
    """Start the FastAPI server"""
    print("Starting FastAPI backend server with web frontend...")
    print("🌐 Frontend: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop")
    print("-" * 60)
    subprocess.run([sys.executable, "FastAPISample.py"])


def launch_mcp():
    """Start the MCP server"""
    if not check_api_running():
        print("❌ Error: FastAPI server is not running!")
        print("\nPlease start it first:")
        print("  python launcher.py api")
        print("\nOr in a separate terminal:")
        print("  python FastAPISample.py")
        sys.exit(1)
    
    print("Starting MCP server...")
    print("Server will communicate via stdio")
    print("Press Ctrl+C to stop")
    print("-" * 60)
    subprocess.run([sys.executable, "MCPSample.py"])


def launch_chat():
    """Run the chat backend example"""
    if not check_api_running():
        print("❌ Error: FastAPI server is not running!")
        print("\nPlease start it first:")
        print("  python launcher.py api")
        sys.exit(1)
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable is not set!")
        print("\nSet it with:")
        print("  Windows PowerShell: $env:OPENAI_API_KEY='your-key-here'")
        print("  Windows CMD: set OPENAI_API_KEY=your-key-here")
        print("  Linux/Mac: export OPENAI_API_KEY=your-key-here")
        print("\nContinuing anyway (will fail if key is required)...")
        print("-" * 60)
    
    print("Running chat backend example...")
    subprocess.run([sys.executable, "ChatBackend.py"])


def run_tests():
    """Run system tests"""
    if not check_api_running():
        print("❌ Error: FastAPI server is not running!")
        print("\nPlease start it first:")
        print("  python launcher.py api")
        print("\nOr in a separate terminal:")
        print("  python FastAPISample.py")
        sys.exit(1)
    
    print("Running system tests...")
    print("-" * 60)
    subprocess.run([sys.executable, "test_system.py"])


def show_all_instructions():
    """Show instructions for running all components"""
    print("\n" + "="*60)
    print("User Search MCP Server - Complete Setup")
    print("="*60)
    print("\nTo run all components, open multiple terminals:\n")
    
    print("Terminal 1 - FastAPI Backend:")
    print("  cd", os.getcwd())
    print("  python launcher.py api")
    print("  (or: python FastAPISample.py)")
    
    print("\nTerminal 2 - MCP Server:")
    print("  cd", os.getcwd())
    print("  python launcher.py mcp")
    print("  (or: python MCPSample.py)")
    
    print("\nTerminal 3 - Chat Backend:")
    print("  cd", os.getcwd())
    print("  $env:OPENAI_API_KEY='your-key-here'  # Set your API key first")
    print("  python launcher.py chat")
    print("  (or: python ChatBackend.py)")
    
    print("\nOr run tests:")
    print("  python launcher.py test")
    print("  (or: python test_system.py)")
    
    print("\n" + "="*60)
    print("For more details, see README.md")
    print("="*60 + "\n")


def main():
    """Main launcher function"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    component = sys.argv[1].lower()
    in ["frontend", "api"]
    if component == "api":
        launch_api()
    elif component == "mcp":
        launch_mcp()
    elif component == "chat":
        launch_chat()
    elif component == "test":
        run_tests()
    elif component == "all":
        show_all_instructions()
    else:
        print(f"❌ Unknown component: {component}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
