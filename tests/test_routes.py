# TODO: Fix tests to run with a local server

# import pytest
# from httpx import AsyncClient
# from .src.main import app

# @pytest.mark.asyncio
# async def test_get_oura_ring_daily_cardiovascular_age():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/oura-ring/daily-cardiovascular-age")  # Replace with actual endpoint
#     assert response.status_code == 200
#     assert "data" in response.json()  # Replace with actual expected key

# @pytest.mark.asyncio
# async def test_get_oura_ring_multiple_daily_activity():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/oura-ring/multiple-daily-activity")  # Replace with actual endpoint
#     assert response.status_code == 200
#     assert "data" in response.json()  # Replace with actual expected key
