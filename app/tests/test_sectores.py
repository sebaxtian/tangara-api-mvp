from fastapi.testclient import TestClient

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals

from app.schemas.sector import SectorSchemaList


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_sectores(tangaras):
    response = client.get("/sectores/")
    sectores = response.json()
    SectorSchemaList.validate({"sectores": sectores})
    # print("sectores:", sectores)

    assert response.status_code == 200
    assert len(sectores) == Totals.SECTORES
