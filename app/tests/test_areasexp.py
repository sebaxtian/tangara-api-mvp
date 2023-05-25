from fastapi.testclient import TestClient

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals

from app.schemas.areaexp import AreaExpSchemaList


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_areasexp(tangaras):
    response = client.get("/areasexp/")
    areasexp = response.json()
    AreaExpSchemaList.validate({"areasexp": areasexp})
    # print("areasexp:", areasexp)

    assert response.status_code == 200
    assert len(areasexp) == Totals.AREASEXP
