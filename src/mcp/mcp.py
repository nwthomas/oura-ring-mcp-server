from mcp.server.fastmcp import FastMCP
from ..constants import SERVER_NAME
import asyncio

mcp = FastMCP(name=SERVER_NAME)

@mcp.tool()
async def get_latest_event():
    """Return the most recent webhook event, if available."""
    try:
        None
        return {"event": None}
    except asyncio.QueueEmpty:
        return {"event": None}