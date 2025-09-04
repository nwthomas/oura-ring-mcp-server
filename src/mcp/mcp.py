from mcp.server.fastmcp import FastMCP
from .constants import SERVER_NAME

mcp = FastMCP(name=SERVER_NAME)

def start_server():
    print(f"Starting {SERVER_NAME}")
    mcp.run(transport='stdio')