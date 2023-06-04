from fastapi.testclient import TestClient
from fastapi import status
import random
from faker import Faker

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals, Codes

from app.schemas.areaexp import AreaExpSchemaList, AreaExpSchema, AreaExpCreate
from app.schemas.tangara import TangaraSchemaList


fake = Faker()
fake.seed_instance('tangara-mvp')


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_areasexp(tangaras):
    response = client.get("/areasexp/")
    areasexp = response.json()
    AreaExpSchemaList.validate({"areasexp": areasexp})
    # print("areasexp:", areasexp)

    assert response.status_code == status.HTTP_200_OK
    assert len(areasexp) == Totals.AREASEXP


def test_get_areasexp_pagination(tangaras):
    response_page1 = client.get(f"/areasexp/?limit={round(Totals.AREASEXP / 2)}&skip=0")
    areasexp_page1 = response_page1.json()
    AreaExpSchemaList.validate({"areasexp": areasexp_page1})

    response_page2 = client.get(f"/areasexp/?limit={round(Totals.AREASEXP / 2)}&skip={round(Totals.AREASEXP / 2)}")
    areasexp_page2 = response_page2.json()
    AreaExpSchemaList.validate({"areasexp": areasexp_page2})

    response_page3 = client.get(f"/areasexp/?limit={Totals.AREASEXP}&skip={Totals.AREASEXP}")
    areasexp_page3 = response_page3.json()
    AreaExpSchemaList.validate({"areasexp": areasexp_page3})

    assert response_page1.status_code == status.HTTP_200_OK
    assert response_page2.status_code == status.HTTP_200_OK
    assert response_page3.status_code == status.HTTP_200_OK
    assert len(areasexp_page1) == round(Totals.AREASEXP / 2)
    assert len(areasexp_page2) == round(Totals.AREASEXP / 2)
    assert len(areasexp_page3) == 0


def test_get_areaexp_by_id(tangaras):
    id_areaexp = random.choice(range(
        Codes.AREAEXP,
        Codes.AREAEXP + Totals.AREASEXP)
    )
    response_found = client.get(f"/areasexp/{id_areaexp}")
    areaexp_found = response_found.json()
    areaexp_found = AreaExpSchema.validate(areaexp_found)
    # print("areaexp_found:", areaexp_found)

    response_not_found = client.get(f"/areasexp/{Codes.VEREDA}")
    areaexp_not_found = response_not_found.json()

    assert response_found.status_code == status.HTTP_200_OK
    assert areaexp_found.id == id_areaexp
    assert response_not_found.status_code == status.HTTP_404_NOT_FOUND
    assert areaexp_not_found["detail"] == "Not Found"


def test_post_areaexp(tangaras):
    areaexp1 = AreaExpCreate(
        id=fake.random_int(min=Codes.AREAEXP + Totals.AREASEXP + 1, max=Codes.AREAPRO),
        nombre=f"AreaExp {fake.unique.street_name()}",
        codigo=f"{fake.unique.bothify(text='???_###').upper()}"
    )
    response1 = client.post(f"/areasexp/", json=areaexp1.dict())

    areaexp2 = areaexp1.copy()
    response2 = client.post(f"/areasexp/", json=areaexp2.dict())

    areaexp3 = areaexp1.copy()
    areaexp3.id = areaexp1.id + 1
    response3 = client.post(f"/areasexp/", json=areaexp3.dict())

    assert response1.status_code == status.HTTP_201_CREATED
    assert areaexp1.id == AreaExpCreate.validate(response1.json()).id
    assert response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response2.json()["detail"] == "AreaExp id must be Unique"
    assert response3.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response3.json()["detail"] == "AreaExp codigo must be Unique"


def test_put_areaexp(tangaras):
    id_areaexp = random.choice(range(
        Codes.AREAEXP,
        Codes.AREAEXP + Totals.AREASEXP)
    )
    response1 = client.get(f"/areasexp/{id_areaexp}")
    areaexp1 = response1.json()
    areaexp1 = AreaExpSchema.validate(areaexp1)

    areaexp1.nombre = f"AreaExp {fake.unique.street_name()}"
    areaexp1.codigo = f"{fake.unique.bothify(text='???_###').upper()}"

    response2 = client.put(f"/areasexp/{id_areaexp}", json=areaexp1.dict())
    areaexp2 = response2.json()
    areaexp2 = AreaExpSchema.validate(areaexp2)

    assert response1.status_code == status.HTTP_200_OK
    assert areaexp1.id == id_areaexp
    assert response2.status_code == status.HTTP_200_OK
    assert areaexp2.id == areaexp1.id
    assert areaexp2.nombre == areaexp1.nombre
    assert areaexp2.codigo == areaexp1.codigo


def test_delete_areaexp(tangaras):
    id_areaexp = random.choice(range(
        Codes.AREAEXP,
        Codes.AREAEXP + Totals.AREASEXP)
    )
    response1 = client.delete(f"/areasexp/{id_areaexp}")

    response2 = client.get(f"/areasexp/{id_areaexp}")

    assert response1.status_code == status.HTTP_204_NO_CONTENT
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert response2.json()["detail"] == "Not Found"


def test_get_tangaras(tangaras):
    id_areaexp = random.choice(range(
        Codes.AREAEXP,
        Codes.AREAEXP + Totals.AREASEXP)
    )
    response = client.get(f"/areasexp/{id_areaexp}/tangaras")
    tangaras = response.json()
    TangaraSchemaList.validate({"tangaras": tangaras})
    # print("tangaras:", tangaras)

    assert response.status_code == status.HTTP_200_OK
