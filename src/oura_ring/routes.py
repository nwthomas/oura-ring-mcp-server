from .constants import OURA_RING_API_BASE, OURA_RING_PERSONAL_ACCESS_TOKEN, SERVER_TIMEOUT_SECONDS, SERVER_USER_AGENT
from httpx import AsyncClient
from typing import Any

def build_oura_ring_request_headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {OURA_RING_PERSONAL_ACCESS_TOKEN}",
        "User-Agent": SERVER_USER_AGENT,
    }

def build_oura_ring_request_params(params: dict[str, Any]) -> dict[str, Any]:
    """This mostly screens out any parameters that have None as their values as this causes
    the Oura Ring API to throw a 400 error.
    """
    return {k: v for k, v in params.items() if v is not None}

async def make_oura_ring_request(url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Make a request to the Oura Ring API with proper error handling."""
    headers = build_oura_ring_request_headers()
    async with AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=SERVER_TIMEOUT_SECONDS)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def get_oura_ring_multiple_daily_activity(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_activity"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)
        
async def get_oura_ring_daily_cardiovascular_age(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_cardiovascular_age"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)

async def get_oura_ring_multiple_daily_readiness(start_date: str, end_date: str, next_token: str | None = None) -> dict[str, Any]:
    url = f"{OURA_RING_API_BASE}/v2/usercollection/daily_readiness"
    params = build_oura_ring_request_params({
        "start_date": start_date,
        "end_date": end_date,
        "next_token": next_token,
    })
    return await make_oura_ring_request(url, params)