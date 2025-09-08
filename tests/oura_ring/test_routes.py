import pytest
from httpx import AsyncClient
from src.oura_ring.routes import get_oura_ring_multiple_daily_activity, get_oura_ring_daily_cardiovascular_age

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_activity_success():
    response = await get_oura_ring_multiple_daily_activity(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_activity_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_daily_activity(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_daily_cardiovascular_age_success():
    response = await get_oura_ring_daily_cardiovascular_age(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_daily_cardiovascular_age_error():
    with pytest.raises(Exception):
        await get_oura_ring_daily_cardiovascular_age(start_date="test-error-start", end_date="test-error-end")
