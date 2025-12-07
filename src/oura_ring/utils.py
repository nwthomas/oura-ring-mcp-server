from httpx import AsyncClient
from typing import Any
from .constants import (
    OURA_RING_PERSONAL_ACCESS_TOKEN,
    SERVER_USER_AGENT,
    SERVER_TIMEOUT_SECONDS,
)
import json
from src.oura_ring.constants import (
    OURA_RING_API_BASE,
    OURA_RING_TOKEN_FILE_NAME,
    OURA_RING_ACCESS_TOKEN_NAME,
    OURA_RING_REFRESH_TOKEN_NAME,
)
import requests

# Cached in-memory tokens during current server runtime
TOKENS = {}


async def load_or_fetch_tokens():
    """Load tokens from file"""
    global TOKENS

    try:
        with open(OURA_RING_TOKEN_FILE_NAME, "r") as f:
            TOKENS = json.load(f)
        if get_access_token() is None or get_refresh_token() is None:
            await fetch_tokens()
    except FileNotFoundError:
        TOKENS = {}


def save_tokens():
    """Save tokens to file"""
    global TOKENS

    with open(OURA_RING_TOKEN_FILE_NAME, "w") as f:
        json.dump(TOKENS, f)


def set_tokens(access_token: str, refresh_token: str):
    """Set tokens in memory and file"""
    global TOKENS

    TOKENS[OURA_RING_ACCESS_TOKEN_NAME] = access_token
    TOKENS[OURA_RING_REFRESH_TOKEN_NAME] = refresh_token
    save_tokens()


def get_access_token() -> str | None:
    """Return current access token"""
    global TOKENS

    return TOKENS.get(OURA_RING_ACCESS_TOKEN_NAME)


def get_refresh_token():
    """Return current refresh token"""
    global TOKENS

    return TOKENS.get(OURA_RING_REFRESH_TOKEN_NAME)


async def fetch_tokens():
    """Ensure TOKENS exist; if not, fetch using the user token."""
    response = requests.post(
        f"{OURA_RING_API_BASE}/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": "<USER_TOKEN_OR_CODE>",
            "client_id": "<CLIENT_ID>",
            "client_secret": "<CLIENT_SECRET>",
            "redirect_uri": "http://localhost:8000/webhook_handler",
        },
    )
    data = response.json()
    TOKENS[OURA_RING_ACCESS_TOKEN_NAME] = data[OURA_RING_ACCESS_TOKEN_NAME]
    TOKENS[OURA_RING_REFRESH_TOKEN_NAME] = data[OURA_RING_REFRESH_TOKEN_NAME]
    save_tokens()


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
