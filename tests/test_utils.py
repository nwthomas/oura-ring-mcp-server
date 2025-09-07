from src.oura_ring.utils import build_oura_ring_request_headers, build_oura_ring_request_params

def test_build_oura_ring_request_headers():
    headers = build_oura_ring_request_headers()
    assert "Accept" in headers
    assert "Authorization" in headers
    assert "User-Agent" in headers

def test_build_oura_ring_request_params():
    params = {"start_date": "2025-09-04", "end_date": None}
    filtered_params = build_oura_ring_request_params(params)
    assert "start_date" in filtered_params
    assert "end_date" not in filtered_params
