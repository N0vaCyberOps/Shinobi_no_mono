import pytest
import httpx
from core.utils.config import load_config

@pytest.mark.asyncio
async def test_http3_connection():
    config = load_config()
    try:
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.get(
                f"http://localhost:{config.get('http3_port', 8000)}/status",
                timeout=5
            )
            assert response.status_code == 200
    except httpx.HTTPError as e:
        pytest.fail(f"HTTP/3 connection failed: {str(e)}")