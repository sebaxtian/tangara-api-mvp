from fastapi.testclient import TestClient
from fastapi import status
import random
from faker import Faker

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals, Codes

from app.schemas.sector import SectorSchemaList, SectorSchema, SectorCreate
from app.schemas.tangara import TangaraSchemaList


fake = Faker()
fake.seed_instance('tangara-mvp')


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_sectores(tangaras):
    response = client.get("/sectores/")
    sectores = response.json()
    SectorSchemaList.validate({"sectores": sectores})
    # print("sectores:", sectores)

    assert response.status_code == status.HTTP_200_OK
    assert len(sectores) == Totals.SECTORES


def test_get_sectores_pagination(tangaras):
    response_page1 = client.get(f"/sectores/?limit={round(Totals.SECTORES / 2)}&skip=0")
    sectores_page1 = response_page1.json()
    SectorSchemaList.validate({"sectores": sectores_page1})

    response_page2 = client.get(f"/sectores/?limit={round(Totals.SECTORES / 2)}&skip={round(Totals.SECTORES / 2)}")
    sectores_page2 = response_page2.json()
    SectorSchemaList.validate({"sectores": sectores_page2})

    response_page3 = client.get(f"/sectores/?limit={Totals.SECTORES}&skip={Totals.SECTORES}")
    sectores_page3 = response_page3.json()
    SectorSchemaList.validate({"sectores": sectores_page3})

    assert response_page1.status_code == status.HTTP_200_OK
    assert response_page2.status_code == status.HTTP_200_OK
    assert response_page3.status_code == status.HTTP_200_OK
    assert len(sectores_page1) == round(Totals.SECTORES / 2)
    assert len(sectores_page2) == round(Totals.SECTORES / 2)
    assert len(sectores_page3) == 0


def test_get_sector_by_id(tangaras):
    id_sector = random.choice(range(
        Codes.SECTOR,
        Codes.SECTOR + Totals.SECTORES)
    )
    response_found = client.get(f"/sectores/{id_sector}")
    sector_found = response_found.json()
    sector_found = SectorSchema.validate(sector_found)
    # print("sector_found:", sector_found)

    response_not_found = client.get(f"/sectores/{Codes.VEREDA}")
    sector_not_found = response_not_found.json()

    assert response_found.status_code == status.HTTP_200_OK
    assert sector_found.id == id_sector
    assert response_not_found.status_code == status.HTTP_404_NOT_FOUND
    assert sector_not_found["detail"] == "Not Found"


def test_post_sector(tangaras):
    id_vereda = random.choice(range(
        Codes.VEREDA,
        Codes.VEREDA + Totals.VEREDAS)
    )
    sector1 = SectorCreate(
        id=fake.random_int(min=Codes.SECTOR + Totals.SECTORES + 1, max=Codes.AREAEXP),
        id_vereda=id_vereda,
        nombre=f"Sector {fake.unique.street_name()}",
        codigo=f"{fake.unique.bothify(text='???_###').upper()}"
    )
    response1 = client.post(f"/sectores/", json=sector1.dict())

    sector2 = sector1.copy()
    response2 = client.post(f"/sectores/", json=sector2.dict())

    sector3 = sector1.copy()
    sector3.id = sector1.id + 1
    response3 = client.post(f"/sectores/", json=sector3.dict())

    assert response1.status_code == status.HTTP_201_CREATED
    assert sector1.id == SectorSchema.validate(response1.json()).id
    assert response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response2.json()["detail"] == "Sector id must be Unique"
    assert response3.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response3.json()["detail"] == "Sector codigo must be Unique"


def test_put_sector(tangaras):
    id_sector = random.choice(range(
        Codes.SECTOR,
        Codes.SECTOR + Totals.SECTORES)
    )
    response1 = client.get(f"/sectores/{id_sector}")
    sector1 = response1.json()
    sector1 = SectorSchema.validate(sector1)

    id_vereda = random.choice(range(
        Codes.VEREDA,
        Codes.VEREDA + Totals.VEREDAS)
    )

    sector1.id_vereda = id_vereda
    sector1.nombre = f"Sector {fake.unique.street_name()}"
    sector1.codigo = f"{fake.unique.bothify(text='???_###').upper()}"

    response2 = client.put(f"/sectores/{id_sector}", json=sector1.dict())
    sector2 = response2.json()
    sector2 = SectorSchema.validate(sector2)

    assert response1.status_code == status.HTTP_200_OK
    assert sector1.id == id_sector
    assert response2.status_code == status.HTTP_200_OK
    assert sector2.id == sector1.id
    assert sector2.id_vereda == sector1.id_vereda
    assert sector2.nombre == sector1.nombre
    assert sector2.codigo == sector1.codigo


def test_delete_sector(tangaras):
    id_sector = random.choice(range(
        Codes.SECTOR,
        Codes.SECTOR + Totals.SECTORES)
    )
    response1 = client.delete(f"/sectores/{id_sector}")

    response2 = client.get(f"/sectores/{id_sector}")

    assert response1.status_code == status.HTTP_204_NO_CONTENT
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert response2.json()["detail"] == "Not Found"


def test_get_tangaras(tangaras):
    id_sector = random.choice(range(
        Codes.SECTOR,
        Codes.SECTOR + Totals.SECTORES)
    )
    response = client.get(f"/sectores/{id_sector}/tangaras")
    tangaras = response.json()
    TangaraSchemaList.validate({"tangaras": tangaras})
    # print("tangaras:", tangaras)

    assert response.status_code == status.HTTP_200_OK
