from fastapi.testclient import TestClient

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals

from app.schemas.tangara import TangaraSchemaList


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_tangaras(tangaras):
    response = client.get("/tangaras/")
    tangaras = response.json()
    TangaraSchemaList.validate({"tangaras": tangaras})
    # print("tangaras:", tangaras)

    assert response.status_code == 200
    assert len(tangaras) == Totals.TANGARAS
