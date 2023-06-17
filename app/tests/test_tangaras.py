from fastapi.testclient import TestClient
from fastapi import status
import random
from faker import Faker

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals, Codes

from app.schemas.tangara import TangaraSchemaList, TangaraSchema, TangaraCreate


fake = Faker()
fake.seed_instance('tangara-mvp')


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_tangaras(tangaras):
    response = client.get("/tangaras/")
    tangaras = response.json()
    TangaraSchemaList.validate({"tangaras": tangaras})
    # print("tangaras:", tangaras)


    assert response.status_code == status.HTTP_200_OK
    assert len(tangaras) == Totals.TANGARAS


def test_get_tangaras_pagination(tangaras):
    response_page1 = client.get(f"/tangaras/?limit={round(Totals.TANGARAS / 2)}&skip=0")
    tangaras_page1 = response_page1.json()
    TangaraSchemaList.validate({"tangaras": tangaras_page1})

    response_page2 = client.get(f"/tangaras/?limit={round(Totals.TANGARAS / 2)}&skip={round(Totals.TANGARAS / 2)}")
    tangaras_page2 = response_page2.json()
    TangaraSchemaList.validate({"tangaras": tangaras_page2})

    response_page3 = client.get(f"/tangaras/?limit={Totals.TANGARAS}&skip={Totals.TANGARAS}")
    tangaras_page3 = response_page3.json()
    TangaraSchemaList.validate({"tangaras": tangaras_page3})


    assert response_page1.status_code == status.HTTP_200_OK
    assert response_page2.status_code == status.HTTP_200_OK
    assert response_page3.status_code == status.HTTP_200_OK
    assert len(tangaras_page1) == round(Totals.TANGARAS / 2)
    assert len(tangaras_page2) == round(Totals.TANGARAS / 2)
    assert len(tangaras_page3) == 0


def test_get_tangara_by_id(tangaras):
    id_tangara = random.choice(range(
        0, Totals.TANGARAS)
    )
    response_found = client.get(f"/tangaras/{id_tangara}")
    tangara_found = response_found.json()
    tangara_found = TangaraSchema.validate(tangara_found)
    # print("tangara_found:", tangara_found)

    response_not_found = client.get(f"/tangaras/{Codes.SECTOR}")
    tangara_not_found = response_not_found.json()


    assert response_found.status_code == status.HTTP_200_OK
    assert tangara_found.id == id_tangara
    assert response_not_found.status_code == status.HTTP_404_NOT_FOUND
    assert tangara_not_found["detail"] == "Not Found"


def _create_tangara(id_tangara) -> dict:
    mac = fake.unique.hexify(text='^^:^^:^^:^^:^^:^^', upper=True)
    dict_tangara = {
        "id": id_tangara,
        "mac": mac,
        "geohash": f"d29{fake.unique.bothify(text='?#?#')}",
        "codigo": f"TANGARA_{mac.split(':')[-2]}{mac.split(':')[-1]}",
        "latitud": fake.unique.latitude(),
        "longitud": fake.unique.longitude(),
        "online": fake.boolean()
    }

    lugar = random.choice(
        [Codes.BARRIO, Codes.SECTOR, Codes.AREAEXP, Codes.AREAPRO]
    )
    total = {Codes.BARRIO: Totals.BARRIOS, Codes.SECTOR: Totals.SECTORES,
                Codes.AREAEXP: Totals.AREASEXP, Codes.AREAPRO: Totals.AREASPRO}
    id_lugar = random.choice(range(
        lugar,
        lugar + total[lugar])
    )

    match lugar:
        case Codes.BARRIO:
            dict_tangara['id_barrio'] = id_lugar
        case Codes.SECTOR:
            dict_tangara['id_sector'] = id_lugar
        case Codes.AREAEXP:
            dict_tangara['id_areaexp'] = id_lugar
        case Codes.AREAPRO:
            dict_tangara['id_areapro'] = id_lugar
        case _:
            pass
    
    return dict_tangara


def test_post_tangara(tangaras):
    tangara1 = TangaraCreate(**_create_tangara(id_tangara=Totals.TANGARAS))
    tangara2 = tangara1.copy()
    tangara3 = tangara1.copy()
    tangara3.id = tangara1.id + 1
    tangara3.id_barrio = Codes.BARRIO
    tangara3.id_sector = Codes.SECTOR
    tangara4 = tangara1.copy()
    tangara4.id = tangara3.id + 1
    tangara5 = tangara1.copy()
    tangara5.id = tangara4.id + 1
    tangara5.mac = fake.unique.hexify(text='^^:^^:^^:^^:^^:^^', upper=True)
    tangara6 = tangara1.copy()
    tangara6.id = tangara5.id + 1
    del tangara6.id_barrio
    del tangara6.id_sector
    del tangara6.id_areaexp
    del tangara6.id_areapro
    tangara7 = tangara6.copy()
    tangara7.id = tangara6.id + 1
    tangara7.id_barrio = 1234567890
    tangara8 = tangara6.copy()
    tangara8.id = tangara6.id + 2
    tangara8.id_sector = 1234567891
    tangara9 = tangara6.copy()
    tangara9.id = tangara6.id + 3
    tangara9.id_areaexp = 1234567892
    tangara10 = tangara6.copy()
    tangara10.id = tangara10.id + 4
    tangara10.id_areapro = 1234567894

    response1 = client.post(f"/tangaras/", json=tangara1.dict())
    response2 = client.post(f"/tangaras/", json=tangara2.dict())
    response3 = client.post(f"/tangaras/", json=tangara3.dict())
    response4 = client.post(f"/tangaras/", json=tangara4.dict())
    response5 = client.post(f"/tangaras/", json=tangara5.dict())
    response6 = client.post(f"/tangaras/", json=tangara6.dict())
    response7 = client.post(f"/tangaras/", json=tangara7.dict())
    response8 = client.post(f"/tangaras/", json=tangara8.dict())
    response9 = client.post(f"/tangaras/", json=tangara9.dict())
    response10 = client.post(f"/tangaras/", json=tangara10.dict())


    assert response1.status_code == status.HTTP_201_CREATED
    assert tangara1.id == TangaraSchema.validate(response1.json()).id
    assert response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response2.json()["detail"] == "Tangara id must be Unique"
    assert response3.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response3.json()["detail"] == "Only one accepted: id_barrio, id_sector, id_areaexp, id_areapro"
    assert response4.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response4.json()["detail"] == "Tangara mac must be Unique"
    assert response5.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response5.json()["detail"] == "Tangara codigo must be Unique"
    assert response6.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response6.json()["detail"] == "Any of id_barrio, id_sector, id_areaexp, id_areapro is required"
    assert response7.status_code == status.HTTP_404_NOT_FOUND
    assert response7.json()["detail"] == "Barrio not found"
    assert response8.status_code == status.HTTP_404_NOT_FOUND
    assert response8.json()["detail"] == "ID Sector Not Found"
    assert response9.status_code == status.HTTP_404_NOT_FOUND
    assert response9.json()["detail"] == "ID AreaExp Not Found"
    assert response10.status_code == status.HTTP_404_NOT_FOUND
    assert response10.json()["detail"] == "ID AreaPro Not Found"


def test_put_tangara(tangaras):
    id_tangara = random.choice(range(
        0,
        Totals.TANGARAS)
    )
    response1 = client.get(f"/tangaras/{id_tangara}")
    tangara1 = response1.json()
    tangara1 = TangaraSchema.validate(tangara1)

    tangara1 = TangaraCreate(**_create_tangara(id_tangara=Totals.TANGARAS))
    tangara1.id = id_tangara

    response2 = client.put(f"/tangaras/{id_tangara}", json=tangara1.dict())
    tangara2 = response2.json()
    tangara2 = TangaraSchema.validate(tangara2)

    
    assert response1.status_code == status.HTTP_200_OK
    assert tangara1.id == id_tangara
    assert response2.status_code == status.HTTP_200_OK
    assert tangara2 == tangara1


def test_delete_tangara(tangaras):
    id_tangara = random.choice(range(
        0,
        Totals.TANGARAS)
    )
    response1 = client.delete(f"/tangaras/{id_tangara}")

    response2 = client.get(f"/tangaras/{id_tangara}")

    assert response1.status_code == status.HTTP_204_NO_CONTENT
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert response2.json()["detail"] == "Not Found"
