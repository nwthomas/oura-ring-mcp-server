from .constants import OURA_RING_API_BASE
from .utils import build_oura_ring_request_params, make_oura_ring_request
from httpx import AsyncClient
from typing import Any

async def get_oura_ring_multiple_daily_activity(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get multiple daily activity values for a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_activity"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)
        
async def get_oura_ring_daily_cardiovascular_age(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get the daily cardiovascular age for a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_cardiovascular_age"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)

async def get_oura_ring_multiple_daily_readiness(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get multiple daily readiness scoresfor a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_readiness"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)

async def get_oura_ring_multiple_daily_resilience(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get multiple daily resilience scores for a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_resilience"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)

async def get_oura_ring_multiple_daily_sleep(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get multiple daily sleep values for a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_sleep"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)

async def get_oura_ring_multiple_daily_spo2(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get multiple daily spo2 values for a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_spo2"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)

async def get_our_ring_multiple_daily_stress(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get multiple daily stress values for a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_stress"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)

async def get_oura_ring_multiple_enhanced_tags(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get multiple daily enhanced tags for a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/enhanced_tag"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)

async def get_oura_ring_multiple_heart_rate(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get multiple daily heart rate values for a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/heartrate"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)

async def get_oura_ring_personal_information() -> dict[str, Any]:
    """Get personal information."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/personal_info"
    return await make_oura_ring_request(url)

async def get_oura_ring_sleep_routes(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    """Get sleep routes for a given date range."""
    url = f"{OURA_RING_API_BASE}/v2/usercollection/sleep"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)