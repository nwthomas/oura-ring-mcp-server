from .mcp import mcp
from .constants import SERVER_PORT

def start_server():
    print(f"Starting MCP server on port {SERVER_PORT}")
    mcp.run(transport='stdio')