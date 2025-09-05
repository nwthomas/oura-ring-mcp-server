from mcp.server.fastmcp import FastMCP
from .constants import SERVER_NAME
from typing import Any
from ..oura_ring.routes import (
    get_oura_ring_daily_cardiovascular_age, 
    get_oura_ring_multiple_daily_activity, 
    get_oura_ring_multiple_daily_readiness,
    get_oura_ring_multiple_daily_resilience,
    get_oura_ring_multiple_daily_sleep,
    get_oura_ring_multiple_daily_spo2,
    get_our_ring_multiple_daily_stress,
    get_oura_ring_multiple_enhanced_tags,
    get_oura_ring_multiple_heart_rate,
    get_oura_ring_personal_information,
    get_oura_ring_sleep_routes
)

mcp = FastMCP(name=SERVER_NAME)

@mcp.tool()
async def get_multiple_daily_activity(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the multiple daily activity for a given date range.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The multiple daily activity for each day in a given date range.
    """
    return await get_oura_ring_multiple_daily_activity(start_date, end_date, next_token)

@mcp.tool()
async def get_daily_cardiovascular_age(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the daily cardiovascular age for a given date range.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The daily cardiovascular age for each day in a given date range.
    """
    return await get_oura_ring_daily_cardiovascular_age(start_date, end_date, next_token)

@mcp.tool()
async def get_multiple_daily_readiness(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the multiple daily readiness for a given date range.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The multiple daily readiness for each day in a given date range.
    """
    return await get_oura_ring_multiple_daily_readiness(start_date, end_date, next_token)

@mcp.tool()
async def get_multiple_daily_resilience(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the multiple daily resilience scores for a given date range.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The multiple daily resilience scores for each day in a given date range.
    """
    return await get_oura_ring_multiple_daily_resilience(start_date, end_date, next_token)

@mcp.tool()
async def get_multiple_daily_sleep(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the multiple daily sleep values for a given date range.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The multiple daily sleep values for each day in a given date range.
    """
    return await get_oura_ring_multiple_daily_sleep(start_date, end_date, next_token)

@mcp.tool()
async def get_multiple_daily_spo2(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the multiple daily spO2 values for a given date range. SpO2 is the oxygen saturation in the blood.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The multiple daily spo2 values for each day in a given date range.
    """
    return await get_oura_ring_multiple_daily_spo2(start_date, end_date, next_token)

@mcp.tool()
async def get_multiple_daily_stress(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the multiple daily stress values for a given date range.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The multiple daily stress values for each day in a given date range.
    """
    return await get_our_ring_multiple_daily_stress(start_date, end_date, next_token)

@mcp.tool()
async def get_multiple_daily_enhanced_tags(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the multiple daily enhanced tags for a given date range.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The multiple daily enhanced tags for each day in a given date range.
    """
    return await get_oura_ring_multiple_enhanced_tags(start_date, end_date, next_token)

@mcp.tool()
async def get_multiple_daily_heart_rate(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the multiple daily heart rate values for a given date range.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The multiple daily heart rate values for each day in a given date range.
    """
    return await get_oura_ring_multiple_heart_rate(start_date, end_date, next_token)

@mcp.tool()
async def get_personal_information() -> dict[str, Any]:
    """Get the personal information about a user (e.g. age, email, weight, and height)."""
    return await get_oura_ring_personal_information()

@mcp.tool()
async def get_sleep_routes(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the sleep data for a given date range. A user can have multiple sleep periods per day.
    
    Args:
        start_date: The start date of the date range. Must be in YYYY-MM-DD format.
        end_date: The end date of the date range. Must be in YYYY-MM-DD format.
        next_token: The next token to use for pagination from a previous request
        
    Returns:
        The sleep routes for each day in a given date range.
    """
    return await get_oura_ring_sleep_routes(start_date, end_date, next_token)

def start_server():
    print(f"Starting {SERVER_NAME}")
    mcp.run(transport='stdio')