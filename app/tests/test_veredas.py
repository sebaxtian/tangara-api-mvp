from fastapi.testclient import TestClient

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals

from app.schemas.vereda import VeredaSchemaList


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_veredas(tangaras):
    response = client.get("/veredas/")
    veredas = response.json()
    VeredaSchemaList.validate({"veredas": veredas})
    # print("veredas:", veredas)

    assert response.status_code == 200
    assert len(veredas) == Totals.VEREDAS
