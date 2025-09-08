import pytest
import pytest_mock
from httpx import AsyncClient
from src.oura_ring.utils import build_oura_ring_request_headers, build_oura_ring_request_params, make_oura_ring_request
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def raise_exception():
    raise Exception("Mocked exception")

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
async def test_make_oura_ring_request_success(mocker: pytest_mock.MockerFixture) -> None:
    url = "https://api.ouraring.com/v2/usercollection/daily_activity"
    params = {"start_date": "2025-09-04", "end_date": "2025-09-04"}
    mock_client = mocker.patch('httpx.AsyncClient', new_callable=AsyncMock)
    mock_response = mock_client.return_value.get.return_value
    mock_response.json = AsyncMock(return_value={'data': [{'mocked_data': 'value'}]})
    mock_response.raise_for_status = MagicMock()  # Mock raise_for_status as a regular MagicMock
    client = mock_client.return_value
    try:
        response = await make_oura_ring_request(client, url, params)
        assert response is not None
        assert "data" in response
    except Exception:
        assert False

@pytest.mark.asyncio
async def test_make_oura_ring_request_error(mocker: pytest_mock.MockerFixture) -> None:
    url = "https://api.ouraring.com/v2/usercollection/daily_activity"
    params = {"start_date": "2025-09-05", "end_date": "2025-09-04"}
    mock_client = mocker.patch('httpx.AsyncClient', new_callable=AsyncMock)
    mock_client.return_value.get.side_effect = raise_exception
    client = mock_client.return_value
    with pytest.raises(Exception):
        await make_oura_ring_request(client, url, params)