from fastapi.testclient import TestClient

# import pytest
# from httpx import AsyncClient
"""
@pytest.mark.anyio
async def test_comunas(comunas):
    async with AsyncClient(app=app, base_url="http://tests") as ac:
        response = await ac.get("/comunas/")

    print("response.json()", response.json())
    assert response.status_code == 200
"""

from app.dependencies.testing_database import override_get_db
from app.main import app, get_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_comunas(comunas):
    response = client.get("/comunas/")
    print("response.json()", response.json())
    assert response.status_code == 200
