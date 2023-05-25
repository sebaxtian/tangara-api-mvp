from fastapi.testclient import TestClient

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals

from app.schemas.areapro import AreaProSchemaList


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_areaspro(tangaras):
    response = client.get("/areaspro/")
    areaspro = response.json()
    AreaProSchemaList.validate({"areaspro": areaspro})
    # print("areaspro:", areaspro)

    assert response.status_code == 200
    assert len(areaspro) == Totals.AREASPRO
