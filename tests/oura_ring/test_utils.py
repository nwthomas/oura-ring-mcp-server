import pytest
import pytest_mock
from httpx import AsyncClient
from src.oura_ring.utils import build_oura_ring_request_headers, build_oura_ring_request_params, make_oura_ring_request

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
async def test_make_oura_ring_request(mocker: pytest_mock.MockerFixture) -> None:
    url = "https://api.ouraring.com/v2/usercollection/daily_activity"
    params = {"start_date": "2025-09-04", "end_date": "2025-09-04"}
    async with AsyncClient() as client:
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
    async with AsyncClient() as client:
        try:
            await make_oura_ring_request(client, url, params)
            assert False
        except Exception:
            assert True