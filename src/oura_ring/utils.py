from httpx import AsyncClient
from typing import Any
from .constants import (
    OURA_RING_USER_CODE,
    OURA_RING_CLIENT_ID,
    OURA_RING_CLIENT_SECRET,
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
import os

# Cached in-memory tokens during current server runtime
TOKENS = {}


async def load_or_fetch_tokens():
    """Load tokens from file"""
    global TOKENS

    try:
        with open(OURA_RING_TOKEN_FILE_NAME, "r") as f:
            TOKENS = json.load(f)
    # This will happen under normal circumstances, so just set the empty variable and continue.
    except FileNotFoundError:
        TOKENS = {}

    print(f"Tokens loaded from file: {TOKENS}")
    # This process either fetches the tokens (realistically, the first time this server is run
    # with a full .env filled out), refreshes the access token, or raises an error. In the error
    # case, the user should get a new user code token from Oura Ring using their OAuth2 flow and
    # and delete the tokens.json file.
    if get_access_token() is None or get_refresh_token() is None:
        try:
            await fetch_tokens()
        except Exception as e:
            print(e)
            raise e
    elif get_refresh_token() is not None:
        await refresh_access_token()
    else:
        # If this case is hit, something has gone wrong with the token process and the user should
        # get and save a new user code token from Oura Ring using their OAuth2 flow.
        delete_tokens()
        raise Exception(
            "No tokens available, please re-run the OAuth2 flow to get a new user code token"
        )


def save_tokens():
    """Save tokens to file"""
    global TOKENS

    with open(OURA_RING_TOKEN_FILE_NAME, "w") as f:
        json.dump(TOKENS, f)


def delete_tokens():
    """Delete tokens.json file"""
    global TOKENS

    TOKENS = {}

    os.remove(OURA_RING_TOKEN_FILE_NAME)


def set_tokens(access_token: str, refresh_token: str):
    """Set tokens in memory and file"""
    global TOKENS

    TOKENS[OURA_RING_ACCESS_TOKEN_NAME] = access_token
    TOKENS[OURA_RING_REFRESH_TOKEN_NAME] = refresh_token


def get_access_token() -> str | None:
    """Return current access token"""
    global TOKENS

    return TOKENS.get(OURA_RING_ACCESS_TOKEN_NAME)


def get_refresh_token():
    """Return current refresh token"""
    global TOKENS

    return TOKENS.get(OURA_RING_REFRESH_TOKEN_NAME)


async def fetch_tokens():
    """Fetch tokens from Oura Ring API"""
    response = requests.post(
        f"{OURA_RING_API_BASE}/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": OURA_RING_USER_CODE,
            "client_id": OURA_RING_CLIENT_ID,
            "client_secret": OURA_RING_CLIENT_SECRET,
        },
    )
    data = response.json()

    if (
        OURA_RING_ACCESS_TOKEN_NAME not in data
        or OURA_RING_REFRESH_TOKEN_NAME not in data
    ):
        raise Exception("No tokens found in response")

    set_tokens(data[OURA_RING_ACCESS_TOKEN_NAME], data[OURA_RING_REFRESH_TOKEN_NAME])
    save_tokens()


async def refresh_access_token():
    """Refresh the access token"""
    response = requests.post(
        f"{OURA_RING_API_BASE}/oauth/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": get_refresh_token(),
            "client_id": OURA_RING_CLIENT_ID,
            "client_secret": OURA_RING_CLIENT_SECRET,
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
        "Authorization": f"Bearer {get_access_token()}",
        "User-Agent": SERVER_USER_AGENT,
    }


def build_oura_ring_request_params(params: dict[str, Any]) -> dict[str, Any]:
    """Builds request params for Oura Ring API requests and filters out None values."""
    return {k: v for k, v in params.items() if v is not None}


async def make_oura_ring_request(
    client: AsyncClient, url: str, params: dict[str, Any] | None = None
) -> dict[str, list[dict[str, Any]]]:
    """Make a request to the Oura Ring API and iteratively fetch results using next_token."""
    all_data = []

    while True:
        try:
            if get_access_token() is None or get_refresh_token() is None:
                await load_or_fetch_tokens()

            headers = build_oura_ring_request_headers()

            response = await client.get(
                url, headers=headers, params=params, timeout=SERVER_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            data = response.json()

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
