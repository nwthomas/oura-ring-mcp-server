def build_oura_ring_request_headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {OURA_RING_PERSONAL_ACCESS_TOKEN}",
        "User-Agent": SERVER_USER_AGENT,
    }

def build_oura_ring_request_params(params: dict[str, Any]) -> dict[str, Any]:
    """builds request params for Oura Ring API requests and filters out None values."""
    return {k: v for k, v in params.items() if v is not None}

async def make_oura_ring_request(url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Make a request to the Oura Ring API with proper error handling."""
    headers = build_oura_ring_request_headers()
    async with AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=SERVER_TIMEOUT_SECONDS)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None