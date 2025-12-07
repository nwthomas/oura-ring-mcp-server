from httpx import AsyncClient
from typing import Any
from .constants import (
    OURA_RING_PERSONAL_ACCESS_TOKEN,
    SERVER_USER_AGENT,
    SERVER_TIMEOUT_SECONDS,
)


def build_oura_ring_request_headers() -> dict[str, str]:
    """Builds request headers for Oura Ring API requests."""
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {OURA_RING_PERSONAL_ACCESS_TOKEN}",
        "User-Agent": SERVER_USER_AGENT,
    }


def build_oura_ring_request_params(params: dict[str, Any]) -> dict[str, Any]:
    """Builds request params for Oura Ring API requests and filters out None values."""
    return {k: v for k, v in params.items() if v is not None}


async def make_oura_ring_request(
    client: AsyncClient, url: str, params: dict[str, Any] | None = None
) -> dict[str, list[dict[str, Any]]]:
    """Make a request to the Oura Ring API and iteratively fetch results using next_token."""
    headers = build_oura_ring_request_headers()
    all_data = []
    while True:
        try:
            response = await client.get(
                url, headers=headers, params=params, timeout=SERVER_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            data = response.json()  # Directly use response.json() without await
            if "data" in data:
                all_data.extend(data["data"])
            else:
                raise Exception("No data found in response")
            next_token = data.get("next_token")
            if not next_token:
                break
            params = params or {}
            params["next_token"] = next_token
        except Exception as error:
            raise error
    return {"data": all_data}
