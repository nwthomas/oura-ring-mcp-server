import pytest
from httpx import AsyncClient
from src.oura_ring.routes import (
    get_oura_ring_daily_cardiovascular_age,
    get_oura_ring_multiple_daily_activity,
    get_oura_ring_multiple_daily_readiness,
    get_oura_ring_multiple_daily_resilience,
    get_oura_ring_multiple_daily_sleep,
    get_oura_ring_multiple_daily_spo2,
    get_oura_ring_multiple_daily_stress,
    get_oura_ring_multiple_enhanced_tags,
    get_oura_ring_multiple_heart_rate,
    get_oura_ring_multiple_session_routes,
    get_oura_ring_multiple_sleep_routes,
    get_oura_ring_multiple_sleep_time,
    get_oura_ring_multiple_vo2_max,
    get_oura_ring_multiple_workout,
    get_oura_ring_personal_information,
)

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

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_readiness_success():
    response = await get_oura_ring_multiple_daily_readiness(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_readiness_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_daily_readiness(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_resilience_success():
    response = await get_oura_ring_multiple_daily_resilience(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_resilience_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_daily_resilience(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_sleep_success():
    response = await get_oura_ring_multiple_daily_sleep(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_sleep_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_daily_sleep(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_spo2_success():
    response = await get_oura_ring_multiple_daily_spo2(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_spo2_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_daily_spo2(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_stress_success():
    response = await get_oura_ring_multiple_daily_stress(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_daily_stress_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_daily_stress(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_enhanced_tags_success():
    response = await get_oura_ring_multiple_enhanced_tags(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_enhanced_tags_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_enhanced_tags(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_heart_rate_success():
    response = await get_oura_ring_multiple_heart_rate(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_heart_rate_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_heart_rate(start_date="test-error-start", end_date="test-error-end")

# @pytest.mark.asyncio
# async def test_get_oura_ring_personal_information_success():
#     response = await get_oura_ring_personal_information()
#     assert response is not None
#     assert "data" in response

# @pytest.mark.asyncio
# async def test_get_oura_ring_personal_information_error():
#     with pytest.raises(Exception):
#         await get_oura_ring_personal_information(client=AsyncClient(base_url="test-error-url"))

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_session_routes_success():
    response = await get_oura_ring_multiple_session_routes(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_session_routes_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_session_routes(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_sleep_routes_success():
    response = await get_oura_ring_multiple_sleep_routes(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_sleep_routes_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_sleep_routes(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_sleep_time_success():
    response = await get_oura_ring_multiple_sleep_time(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_sleep_time_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_sleep_time(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_vo2_max_success():
    response = await get_oura_ring_multiple_vo2_max(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_vo2_max_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_vo2_max(start_date="test-error-start", end_date="test-error-end")

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_workout_success():
    response = await get_oura_ring_multiple_workout(start_date="2025-01-01", end_date="2025-01-01")
    assert response is not None
    assert "data" in response

@pytest.mark.asyncio
async def test_get_oura_ring_multiple_workout_error():
    with pytest.raises(Exception):
        await get_oura_ring_multiple_workout(start_date="test-error-start", end_date="test-error-end")