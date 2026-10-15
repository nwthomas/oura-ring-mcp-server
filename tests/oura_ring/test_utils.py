from unittest.mock import AsyncMock, MagicMock

import stat
from pathlib import Path

import pytest
import pytest_mock

from src.oura_ring.utils import (
    OuraRingAuthError,
    build_oura_ring_request_headers,
    build_oura_ring_request_params,
    fetch_tokens,
    get_refresh_token,
    make_oura_ring_request,
    refresh_access_token,
    save_tokens,
    set_tokens,
)


@pytest.mark.asyncio
async def raise_runtime_error(*_args, **_kwargs):
    raise RuntimeError("Mocked exception")


def test_build_oura_ring_request_headers() -> None:
    headers = build_oura_ring_request_headers()
    assert "Accept" in headers
    assert "Authorization" in headers
    assert "User-Agent" in headers


def test_build_oura_ring_request_params_no_filtering() -> None:
    params = {"start_date": "2025-09-04", "end_date": "2025-09-04"}
    filtered_params = build_oura_ring_request_params(params)
    assert "start_date" in filtered_params
    assert "end_date" in filtered_params


def test_build_oura_ring_request_params_filter_none_values() -> None:
    params = {"start_date": "2025-09-04", "end_date": None}
    filtered_params = build_oura_ring_request_params(params)
    assert "start_date" in filtered_params
    assert "end_date" not in filtered_params


@pytest.mark.asyncio
async def test_make_oura_ring_request_success(
    mocker: pytest_mock.MockerFixture, mock_token_response: MagicMock
) -> None:
    url = "https://api.ouraring.com/v2/usercollection/daily_activity"
    params = {"start_date": "2025-09-04", "end_date": "2025-09-04"}
    mock_client = mocker.patch("httpx.AsyncClient", new_callable=AsyncMock)
    mock_response = mock_client.return_value.get.return_value
    mock_response.json = MagicMock(return_value={"data": [{"mocked_data": "value"}]})
    mock_response.raise_for_status = MagicMock()
    mocker.patch("src.oura_ring.utils.requests.post", return_value=mock_token_response)

    response = await make_oura_ring_request(mock_client.return_value, url, params)

    assert response is not None
    assert "data" in response


@pytest.mark.asyncio
async def test_make_oura_ring_request_error(
    mocker: pytest_mock.MockerFixture, mock_token_response: MagicMock
) -> None:
    url = "https://api.ouraring.com/v2/usercollection/daily_activity"
    params = {"start_date": "2025-09-05", "end_date": "2025-09-04"}
    mock_client = mocker.patch("httpx.AsyncClient", new_callable=AsyncMock)
    mock_client.return_value.get.side_effect = raise_runtime_error
    mocker.patch("src.oura_ring.utils.requests.post", return_value=mock_token_response)

    with pytest.raises(RuntimeError):
        await make_oura_ring_request(mock_client.return_value, url, params)


@pytest.mark.asyncio
async def test_fetch_tokens_includes_redirect_uri(
    mocker: pytest_mock.MockerFixture, mock_token_response: MagicMock
) -> None:
    mock_post = mocker.patch(
        "src.oura_ring.utils.requests.post", return_value=mock_token_response
    )
    mocker.patch("src.oura_ring.utils.OURA_RING_REDIRECT_URI", "https://example.test")

    await fetch_tokens()

    payload = mock_post.call_args.kwargs["data"]
    assert payload["grant_type"] == "authorization_code"
    assert payload["redirect_uri"] == "https://example.test"


@pytest.mark.asyncio
async def test_refresh_access_token_excludes_redirect_uri(
    mocker: pytest_mock.MockerFixture, mock_token_response: MagicMock
) -> None:
    set_tokens("stale_access", "stale_refresh")
    mock_post = mocker.patch(
        "src.oura_ring.utils.requests.post", return_value=mock_token_response
    )

    await refresh_access_token()

    payload = mock_post.call_args.kwargs["data"]
    assert payload["grant_type"] == "refresh_token"
    assert payload["refresh_token"] == "stale_refresh"
    assert "redirect_uri" not in payload


@pytest.mark.asyncio
async def test_refresh_access_token_raises_on_invalid_grant(
    mocker: pytest_mock.MockerFixture,
) -> None:
    set_tokens("stale_access", "stale_refresh")
    mocker.patch(
        "src.oura_ring.utils.requests.post",
        return_value=MagicMock(
            status_code=400,
            json=MagicMock(
                return_value={
                    "error": "invalid_grant",
                    "error_description": "Refresh token is invalid.",
                }
            ),
        ),
    )

    with pytest.raises(OuraRingAuthError, match="invalid_grant"):
        await refresh_access_token()

    assert get_refresh_token() is None


@pytest.mark.asyncio
async def test_refresh_access_token_keeps_tokens_on_invalid_client(
    mocker: pytest_mock.MockerFixture,
) -> None:
    set_tokens("stale_access", "stale_refresh")
    mocker.patch(
        "src.oura_ring.utils.requests.post",
        return_value=MagicMock(
            status_code=400,
            json=MagicMock(
                return_value={
                    "error": "invalid_client",
                    "error_description": "Client credentials are invalid.",
                }
            ),
        ),
    )

    with pytest.raises(OuraRingAuthError, match="invalid_client"):
        await refresh_access_token()

    assert get_refresh_token() == "stale_refresh"


@pytest.mark.asyncio
async def test_make_oura_ring_request_returns_bare_object_for_personal_info(
    mocker: pytest_mock.MockerFixture,
) -> None:
    url = "https://api.ouraring.com/v2/usercollection/personal_info"
    set_tokens("access", "refresh")
    mock_client = mocker.patch("httpx.AsyncClient", new_callable=AsyncMock)
    mock_response = mock_client.return_value.get.return_value
    mock_response.json = MagicMock(return_value={"id": "abc", "age": 31})
    mock_response.raise_for_status = MagicMock()

    response = await make_oura_ring_request(mock_client.return_value, url)

    assert response == {"id": "abc", "age": 31}


@pytest.mark.asyncio
async def test_fetch_tokens_missing_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("src.oura_ring.utils.OURA_RING_CLIENT_ID", "")

    with pytest.raises(OuraRingAuthError, match="OURA_RING_CLIENT_ID"):
        await fetch_tokens()


def test_save_tokens_sets_restricted_permissions() -> None:
    """OAuth tokens on disk must be readable only by the owner."""
    set_tokens("test_access", "test_refresh")
    save_tokens()

    from src.oura_ring.utils import OURA_RING_TOKEN_FILE_NAME

    mode = stat.S_IMODE(Path(OURA_RING_TOKEN_FILE_NAME).stat().st_mode)
    assert mode == 0o600
