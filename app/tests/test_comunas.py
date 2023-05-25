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

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals

from app.schemas.comuna import ComunaSchemaList


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_comunas(tangaras):
    response = client.get("/comunas/")
    comunas = response.json()
    ComunaSchemaList.validate({"comunas": comunas})
    # print("comunas:", comunas)

    assert response.status_code == 200
    assert len(comunas) == Totals.COMUNAS
