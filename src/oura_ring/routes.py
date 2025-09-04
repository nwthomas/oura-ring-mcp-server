from .constants import OURA_RING_PERSONAL_ACCESS_TOKEN, SERVER_TIMEOUT_SECONDS, SERVER_USER_AGENT
from httpx import AsyncClient
from typing import Any

async def make_oura_ring_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Oura Ring API with proper error handling."""
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {OURA_RING_PERSONAL_ACCESS_TOKEN}",
        "User-Agent": SERVER_USER_AGENT,
    }
    async with AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=SERVER_TIMEOUT_SECONDS)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
async def get_daily_cardiovascular_age() -> dict[str, Any]:
    pass