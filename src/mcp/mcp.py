from mcp.server.fastmcp import FastMCP
from .constants import SERVER_NAME
from typing import Any
from ..oura_ring.routes import get_oura_ring_daily_cardiovascular_age

mcp = FastMCP(name=SERVER_NAME)

@mcp.tool()
async def get_daily_cardiovascular_age(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the daily cardiovascular age for a given date range.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The daily cardiovascular age for the given date range.
    """
    return await get_oura_ring_daily_cardiovascular_age(start_date, end_date, next_token)
    

def start_server():
    print(f"Starting {SERVER_NAME}")
    mcp.run(transport='stdio')