from fastapi.testclient import TestClient
from fastapi import status
import random
from faker import Faker

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals, Codes

from app.schemas.areapro import AreaProSchemaList, AreaProSchema, AreaProCreate
from app.schemas.tangara import TangaraSchemaList


fake = Faker()
fake.seed_instance('tangara-mvp')


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_areaspro(tangaras):
    response = client.get("/areaspro/")
    areaspro = response.json()
    AreaProSchemaList.validate({"areaspro": areaspro})
    # print("areaspro:", areaspro)

    assert response.status_code == status.HTTP_200_OK
    assert len(areaspro) == Totals.AREASPRO


def test_get_areaspro_pagination(tangaras):
    response_page1 = client.get(f"/areaspro/?limit={round(Totals.AREASPRO / 2)}&skip=0")
    areaspro_page1 = response_page1.json()
    AreaProSchemaList.validate({"areaspro": areaspro_page1})

    response_page2 = client.get(f"/areaspro/?limit={round(Totals.AREASPRO / 2)}&skip={round(Totals.AREASPRO / 2)}")
    areaspro_page2 = response_page2.json()
    AreaProSchemaList.validate({"areaspro": areaspro_page2})

    response_page3 = client.get(f"/areaspro/?limit={Totals.AREASPRO}&skip={Totals.AREASPRO}")
    areaspro_page3 = response_page3.json()
    AreaProSchemaList.validate({"areaspro": areaspro_page3})

    assert response_page1.status_code == status.HTTP_200_OK
    assert response_page2.status_code == status.HTTP_200_OK
    assert response_page3.status_code == status.HTTP_200_OK
    assert len(areaspro_page1) == round(Totals.AREASPRO / 2)
    assert len(areaspro_page2) == round(Totals.AREASPRO / 2) - 1
    assert len(areaspro_page3) == 0


def test_get_areapro_by_id(tangaras):
    id_areapro = random.choice(range(
        Codes.AREAPRO,
        Codes.AREAPRO + Totals.AREASPRO)
    )
    response_found = client.get(f"/areaspro/{id_areapro}")
    areapro_found = response_found.json()
    areapro_found = AreaProSchema.validate(areapro_found)
    # print("areapro_found:", areapro_found)

    response_not_found = client.get(f"/areaspro/{Codes.COMUNA}")
    areapro_not_found = response_not_found.json()

    assert response_found.status_code == status.HTTP_200_OK
    assert areapro_found.id == id_areapro
    assert response_not_found.status_code == status.HTTP_404_NOT_FOUND
    assert areapro_not_found["detail"] == "Not Found"


def test_post_areapro(tangaras):
    areapro1 = AreaProCreate(
        id=fake.random_int(min=Codes.AREAPRO + Totals.AREASPRO + 1, max=Codes.AREAPRO + 1000),
        nombre=f"AreaPro {fake.unique.street_name()}",
        codigo=f"{fake.unique.bothify(text='???_###').upper()}"
    )
    response1 = client.post(f"/areaspro/", json=areapro1.dict())

    areapro2 = areapro1.copy()
    response2 = client.post(f"/areaspro/", json=areapro2.dict())

    areapro3 = areapro1.copy()
    areapro3.id = areapro1.id + 1
    response3 = client.post(f"/areaspro/", json=areapro3.dict())

    assert response1.status_code == status.HTTP_201_CREATED
    assert areapro1.id == AreaProCreate.validate(response1.json()).id
    assert response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response2.json()["detail"] == "AreaPro id must be Unique"
    assert response3.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response3.json()["detail"] == "AreaPro codigo must be Unique"


def test_put_areapro(tangaras):
    id_areapro = random.choice(range(
        Codes.AREAPRO,
        Codes.AREAPRO + Totals.AREASPRO)
    )
    response1 = client.get(f"/areaspro/{id_areapro}")
    areapro1 = response1.json()
    areapro1 = AreaProSchema.validate(areapro1)

    areapro1.nombre = f"AreaPro {fake.unique.street_name()}"
    areapro1.codigo = f"{fake.unique.bothify(text='???_###').upper()}"

    response2 = client.put(f"/areaspro/{id_areapro}", json=areapro1.dict())
    areapro2 = response2.json()
    areapro2 = AreaProSchema.validate(areapro2)

    assert response1.status_code == status.HTTP_200_OK
    assert areapro1.id == id_areapro
    assert response2.status_code == status.HTTP_200_OK
    assert areapro2.id == areapro1.id
    assert areapro2.nombre == areapro1.nombre
    assert areapro2.codigo == areapro1.codigo


def test_delete_areapro(tangaras):
    id_areapro = random.choice(range(
        Codes.AREAPRO,
        Codes.AREAPRO + Totals.AREASPRO)
    )
    response1 = client.delete(f"/areaspro/{id_areapro}")

    response2 = client.get(f"/areaspro/{id_areapro}")

    assert response1.status_code == status.HTTP_204_NO_CONTENT
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert response2.json()["detail"] == "Not Found"


def test_get_tangaras(tangaras):
    id_areapro = random.choice(range(
        Codes.AREAPRO,
        Codes.AREAPRO + Totals.AREASPRO)
    )
    response = client.get(f"/areaspro/{id_areapro}/tangaras")
    tangaras = response.json()
    TangaraSchemaList.validate({"tangaras": tangaras})
    # print("tangaras:", tangaras)

    assert response.status_code == status.HTTP_200_OK
