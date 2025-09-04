from mcp.server.fastmcp import FastMCP
from .constants import SERVER_NAME

mcp = FastMCP(SERVER_NAME)

def start_server():
    mcp.run(transport='stdio')