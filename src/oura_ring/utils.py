import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests
from httpx import AsyncClient, HTTPStatusError

from src.oura_ring.constants import (
    OURA_RING_ACCESS_TOKEN_NAME,
    OURA_RING_CLIENT_ID,
    OURA_RING_CLIENT_SECRET,
    OURA_RING_OAUTH_TOKEN_URL,
    OURA_RING_REDIRECT_URI,
    OURA_RING_REFRESH_TOKEN_NAME,
    OURA_RING_TOKEN_FILE_NAME,
    OURA_RING_USER_CODE,
    SERVER_TIMEOUT_SECONDS,
    SERVER_USER_AGENT,
)

# Cached in-memory tokens during current server runtime
TOKENS = {}
TOKEN_REFRESH_LOCK = asyncio.Lock()


class OuraRingAuthError(RuntimeError):
    """Raised when Oura OAuth token exchange or refresh fails."""

    def __init__(self, message: str, error_code: str | None = None):
        super().__init__(message)
        self.error_code = error_code


async def load_or_fetch_tokens():
    """Load tokens from disk, or exchange the configured auth code on first run."""
    if get_access_token() is not None and get_refresh_token() is not None:
        return

    try:
        with open(OURA_RING_TOKEN_FILE_NAME, "r", encoding="utf-8") as token_file:
            TOKENS.clear()
            TOKENS.update(json.load(token_file))
    except FileNotFoundError:
        TOKENS.clear()

    print(f"Tokens loaded from file (present: {bool(TOKENS)})", file=sys.stderr)

    if get_access_token() is None or get_refresh_token() is None:
        await fetch_tokens()


def save_tokens():
    """Save tokens to disk with an atomic replace."""
    token_path = Path(OURA_RING_TOKEN_FILE_NAME)
    temporary_path = token_path.with_name(f".{token_path.name}.tmp")

    with open(temporary_path, "w", encoding="utf-8") as token_file:
        json.dump(TOKENS, token_file)
    os.replace(temporary_path, token_path)


def delete_tokens():
    """Delete tokens from memory and disk."""
    TOKENS.clear()

    try:
        os.remove(OURA_RING_TOKEN_FILE_NAME)
    except FileNotFoundError:
        pass


def set_tokens(access_token: str, refresh_token: str):
    """Set tokens in memory."""
    TOKENS[OURA_RING_ACCESS_TOKEN_NAME] = access_token
    TOKENS[OURA_RING_REFRESH_TOKEN_NAME] = refresh_token


def get_access_token() -> str | None:
    """Return current access token."""
    return TOKENS.get(OURA_RING_ACCESS_TOKEN_NAME)


def get_refresh_token() -> str | None:
    """Return current refresh token."""
    return TOKENS.get(OURA_RING_REFRESH_TOKEN_NAME)


def _raise_for_token_error(response: requests.Response, data: dict[str, Any]) -> None:
    """Raise a useful auth error for OAuth error responses."""
    if response.status_code < 400:
        return

    error = data.get("error", "unknown_error")
    description = data.get("error_description", "No error description provided.")
    raise OuraRingAuthError(
        f"Oura token request failed ({response.status_code} {error}): {description}",
        error_code=error,
    )


def _post_token_request(payload: dict[str, Any]) -> dict[str, Any]:
    """Send an OAuth token request and return the parsed JSON body."""
    response = requests.post(
        OURA_RING_OAUTH_TOKEN_URL,
        data=payload,
        timeout=SERVER_TIMEOUT_SECONDS,
    )

    try:
        data = response.json()
    except requests.JSONDecodeError as error:
        raise OuraRingAuthError(
            f"Oura token request returned non-JSON response ({response.status_code})"
        ) from error

    _raise_for_token_error(response, data)
    return data


def _require_token_pair(data: dict[str, Any], action: str) -> tuple[str, str]:
    """Extract a token pair or raise a clear error."""
    if (
        OURA_RING_ACCESS_TOKEN_NAME not in data
        or OURA_RING_REFRESH_TOKEN_NAME not in data
    ):
        raise OuraRingAuthError(
            f"Oura {action} response did not include an access/refresh token pair."
        )

    return data[OURA_RING_ACCESS_TOKEN_NAME], data[OURA_RING_REFRESH_TOKEN_NAME]


async def fetch_tokens():
    """Fetch tokens from Oura Ring API."""
    payload = {
        "grant_type": "authorization_code",
        "code": OURA_RING_USER_CODE,
        "client_id": OURA_RING_CLIENT_ID,
        "client_secret": OURA_RING_CLIENT_SECRET,
    }
    if OURA_RING_REDIRECT_URI:
        payload["redirect_uri"] = OURA_RING_REDIRECT_URI

    access_token, refresh_token = _require_token_pair(
        _post_token_request(payload), "authorization-code exchange"
    )
    set_tokens(access_token, refresh_token)
    save_tokens()


async def refresh_access_token():
    """Refresh and persist the access/refresh token pair."""
    async with TOKEN_REFRESH_LOCK:
        if get_refresh_token() is None:
            await load_or_fetch_tokens()

        try:
            access_token, refresh_token = _require_token_pair(
                _post_token_request(
                    {
                        "grant_type": "refresh_token",
                        "refresh_token": get_refresh_token(),
                        "client_id": OURA_RING_CLIENT_ID,
                        "client_secret": OURA_RING_CLIENT_SECRET,
                    }
                ),
                "refresh",
            )
        except OuraRingAuthError as error:
            if error.error_code == "invalid_grant":
                delete_tokens()
            raise

        set_tokens(access_token, refresh_token)
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


async def _refresh_after_unauthorized(
    client: AsyncClient, url: str, params: dict[str, Any]
):
    """Refresh the token and retry an API request once after a 401."""
    await refresh_access_token()
    return await client.get(
        url,
        headers=build_oura_ring_request_headers(),
        params=params,
        timeout=SERVER_TIMEOUT_SECONDS,
    )


async def make_oura_ring_request(
    client: AsyncClient, url: str, params: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Make a request to the Oura Ring API and iteratively fetch results using next_token."""
    all_data = []
    request_params = dict(params or {})

    while True:
        if get_access_token() is None or get_refresh_token() is None:
            await load_or_fetch_tokens()

        response = await client.get(
            url,
            headers=build_oura_ring_request_headers(),
            params=request_params,
            timeout=SERVER_TIMEOUT_SECONDS,
        )

        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            if error.response.status_code != 401:
                raise

            response = await _refresh_after_unauthorized(client, url, request_params)
            response.raise_for_status()

        data = response.json()

        if "data" not in data:
            return data

        all_data.extend(data["data"])
        next_token = data.get("next_token")
        if not next_token:
            break

        request_params["next_token"] = next_token

    return {"data": all_data}
