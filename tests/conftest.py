from unittest.mock import MagicMock

import pytest

from src.oura_ring import utils


@pytest.fixture(autouse=True)
def isolate_token_file(tmp_path, monkeypatch):
    """Keep mocked tests from reading or overwriting the real token file."""
    monkeypatch.setattr(
        utils, "OURA_RING_TOKEN_FILE_NAME", str(tmp_path / "tokens.json")
    )
    monkeypatch.setattr(utils, "TOKENS", {})
    # Dummy OAuth credentials so mocked tests pass credential validation.
    monkeypatch.setattr(utils, "OURA_RING_CLIENT_ID", "test_client_id")
    monkeypatch.setattr(utils, "OURA_RING_CLIENT_SECRET", "test_client_secret")
    monkeypatch.setattr(utils, "OURA_RING_USER_CODE", "test_user_code")


@pytest.fixture
def mock_token_response():
    """Return a successful mocked OAuth token response."""
    return MagicMock(
        status_code=200,
        json=MagicMock(
            return_value={
                "access_token": "mock_access_token",
                "refresh_token": "mock_refresh_token",
            }
        ),
    )
