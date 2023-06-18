from fastapi.testclient import TestClient

# import pytest
# from httpx import AsyncClient
"""
@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=app, base_url="http://tests") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tangara API MVP", "environment": "test"}
"""

from app.main import app


client = TestClient(app)


def test_root(men_cache):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tangara API MVP", "environment": "dev"}
