from fastapi.testclient import TestClient

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals

from app.schemas.barrio import BarrioSchemaList


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_barrios(tangaras):
    response = client.get("/barrios/")
    barrios = response.json()
    BarrioSchemaList.validate({"barrios": barrios})
    # print("barrios:", barrios)

    assert response.status_code == 200
    assert len(barrios) == Totals.BARRIOS
