from fastapi.testclient import TestClient
from fastapi import status
import random
from faker import Faker

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals, Codes

from app.schemas.vereda import VeredaSchemaList, VeredaSchema, VeredaCreate
from app.schemas.sector import SectorSchemaList
from app.schemas.tangara import TangaraSchemaList


fake = Faker()
fake.seed_instance('tangara-mvp')


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_veredas(tangaras):
    response = client.get("/veredas/")
    veredas = response.json()
    VeredaSchemaList.validate({"veredas": veredas})
    # print("veredas:", veredas)

    assert response.status_code == status.HTTP_200_OK
    assert len(veredas) == Totals.VEREDAS


def test_get_veredas_pagination(tangaras):
    response_page1 = client.get(f"/veredas/?limit={round(Totals.VEREDAS / 2)}&skip=0")
    veredas_page1 = response_page1.json()
    VeredaSchemaList.validate({"veredas": veredas_page1})

    response_page2 = client.get(f"/veredas/?limit={round(Totals.VEREDAS / 2)}&skip={round(Totals.VEREDAS / 2)}")
    veredas_page2 = response_page2.json()
    VeredaSchemaList.validate({"veredas": veredas_page2})

    response_page3 = client.get(f"/veredas/?limit={Totals.VEREDAS}&skip={Totals.VEREDAS}")
    veredas_page3 = response_page3.json()
    VeredaSchemaList.validate({"veredas": veredas_page3})

    assert response_page1.status_code == status.HTTP_200_OK
    assert response_page2.status_code == status.HTTP_200_OK
    assert response_page3.status_code == status.HTTP_200_OK
    assert len(veredas_page1) == round(Totals.VEREDAS / 2)
    assert len(veredas_page2) == round(Totals.VEREDAS / 2)
    assert len(veredas_page3) == 0


def test_get_vereda_by_id(tangaras):
    id_vereda = random.choice(range(
        Codes.VEREDA,
        Codes.VEREDA + Totals.VEREDAS)
    )
    response_found = client.get(f"/veredas/{id_vereda}")
    vereda_found = response_found.json()
    vereda_found = VeredaSchema.validate(vereda_found)
    # print("vereda_found:", vereda_found)

    response_not_found = client.get(f"/veredas/{Codes.SECTOR}")
    vereda_not_found = response_not_found.json()

    assert response_found.status_code == status.HTTP_200_OK
    assert vereda_found.id == id_vereda
    assert response_not_found.status_code == status.HTTP_404_NOT_FOUND
    assert vereda_not_found["detail"] == "Not Found"


def test_post_vereda(tangaras):
    vereda1 = VeredaCreate(
        id=fake.random_int(min=Codes.VEREDA + Totals.VEREDAS + 1, max=Codes.SECTOR), 
        nombre=f"Vereda {fake.unique.bothify(text='###')}", 
        codigo=f"{fake.unique.bothify(text='???_###').upper()}"
    )
    response1 = client.post(f"/veredas/", json=vereda1.dict())

    vereda2 = vereda1.copy()
    response2 = client.post(f"/veredas/", json=vereda2.dict())

    vereda3 = vereda1.copy()
    vereda3.id = vereda1.id + 1
    response3 = client.post(f"/veredas/", json=vereda3.dict())

    assert response1.status_code == status.HTTP_201_CREATED
    assert vereda1.id == VeredaSchema.validate(response1.json()).id
    assert response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response2.json()["detail"] == "Vereda id must be Unique"
    assert response3.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response3.json()["detail"] == "Vereda codigo must be Unique"


def test_put_vereda(tangaras):
    id_vereda = random.choice(range(
        Codes.VEREDA,
        Codes.VEREDA + Totals.VEREDAS)
    )
    response1 = client.get(f"/veredas/{id_vereda}")
    vereda1 = response1.json()
    vereda1 = VeredaSchema.validate(vereda1)

    vereda1.nombre = f"Vereda {fake.unique.bothify(text='###')}"
    vereda1.codigo = f"{fake.unique.bothify(text='???_###').upper()}"

    response2 = client.put(f"/veredas/{id_vereda}", json=vereda1.dict())
    vereda2 = response2.json()
    vereda2 = VeredaSchema.validate(vereda2)


    assert response1.status_code == status.HTTP_200_OK
    assert vereda1.id == id_vereda
    assert response2.status_code == status.HTTP_200_OK
    assert vereda2.id == vereda1.id
    assert vereda2.nombre == vereda1.nombre
    assert vereda2.codigo == vereda1.codigo


def test_delete_vereda(tangaras):
    id_vereda = random.choice(range(
        Codes.VEREDA,
        Codes.VEREDA + Totals.VEREDAS)
    )
    response1 = client.delete(f"/veredas/{id_vereda}")

    response2 = client.get(f"/veredas/{id_vereda}")

    assert response1.status_code == status.HTTP_204_NO_CONTENT
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert response2.json()["detail"] == "Not Found"


def test_get_veredas_sectores(tangaras):
    id_vereda = random.choice(range(
        Codes.VEREDA,
        Codes.VEREDA + Totals.VEREDAS)
    )
    response = client.get(f"/veredas/{id_vereda}/sectores")
    sectores = response.json()
    SectorSchemaList.validate({"sectores": sectores})
    # print("sectores:", sectores)

    assert response.status_code == status.HTTP_200_OK


def test_get_veredas_tangaras(tangaras):
    id_vereda = random.choice(range(
        Codes.VEREDA,
        Codes.VEREDA + Totals.VEREDAS)
    )
    response = client.get(f"/veredas/{id_vereda}/tangaras")
    tangaras = response.json()
    TangaraSchemaList.validate({"tangaras": tangaras})
    # print("tangaras:", tangaras)

    assert response.status_code == status.HTTP_200_OK
