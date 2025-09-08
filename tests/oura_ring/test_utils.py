import pytest
import pytest_mock
from httpx import AsyncClient
from src.oura_ring.utils import build_oura_ring_request_headers, build_oura_ring_request_params, make_oura_ring_request

def test_build_oura_ring_request_headers() -> None:
    headers = build_oura_ring_request_headers()
    assert "Accept" in headers
    assert "Authorization" in headers
    assert "User-Agent" in headers

def test_build_oura_ring_request_params() -> None:
    params = {"start_date": "2025-09-04", "end_date": None}
    filtered_params = build_oura_ring_request_params(params)
    assert "start_date" in filtered_params
    assert "end_date" not in filtered_params

@pytest.mark.asyncio
async def test_make_oura_ring_request(mocker: pytest_mock.MockerFixture) -> None:
    url = "https://api.oura.com/v2/usercollection/daily_activity"
    params = {"start_date": "2025-09-04", "end_date": None}
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "mocked_data"}
    async with AsyncClient() as client:
        mocker.patch.object(client, 'get', return_value=mock_response)
        response = await client.get(url, params=params)
        assert response is not None
        assert "data" in response.json()
        assert response.status_code == 200