from fastapi.testclient import TestClient
from fastapi import status
import random
from faker import Faker

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals, Codes

from app.schemas.barrio import BarrioSchemaList, BarrioSchema, BarrioCreate
from app.schemas.tangara import TangaraSchemaList


fake = Faker()
fake.seed_instance('tangara-mvp')


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_barrios(tangaras):
    response = client.get("/barrios/")
    barrios = response.json()
    BarrioSchemaList.validate({"barrios": barrios})
    # print("barrios:", barrios)

    assert response.status_code == status.HTTP_200_OK
    assert len(barrios) == Totals.BARRIOS


def test_get_barrios_pagination(tangaras):
    response_page1 = client.get(f"/barrios/?limit={round(Totals.BARRIOS / 2)}&skip=0")
    barrios_page1 = response_page1.json()
    BarrioSchemaList.validate({"barrios": barrios_page1})

    response_page2 = client.get(f"/barrios/?limit={round(Totals.BARRIOS / 2)}&skip={round(Totals.BARRIOS / 2)}")
    barrios_page2 = response_page2.json()
    BarrioSchemaList.validate({"barrios": barrios_page2})

    response_page3 = client.get(f"/barrios/?limit={Totals.BARRIOS}&skip={Totals.BARRIOS}")
    barrios_page3 = response_page3.json()
    BarrioSchemaList.validate({"barrios": barrios_page3})

    assert response_page1.status_code == status.HTTP_200_OK
    assert response_page2.status_code == status.HTTP_200_OK
    assert response_page3.status_code == status.HTTP_200_OK
    assert len(barrios_page1) == round(Totals.BARRIOS / 2)
    assert len(barrios_page2) == round(Totals.BARRIOS / 2)
    assert len(barrios_page3) == 0


def test_get_barrio_by_id(tangaras):
    id_barrio = random.choice(range(
        Codes.BARRIO,
        Codes.BARRIO + Totals.BARRIOS)
    )
    response_found = client.get(f"/barrios/{id_barrio}")
    barrio_found = response_found.json()
    barrio_found = BarrioSchema.validate(barrio_found)
    # print("barrio_found:", barrio_found)

    response_not_found = client.get(f"/barrios/{Codes.COMUNA}")
    barrio_not_found = response_not_found.json()

    assert response_found.status_code == status.HTTP_200_OK
    assert barrio_found.id == id_barrio
    assert response_not_found.status_code == status.HTTP_404_NOT_FOUND
    assert barrio_not_found["detail"] == "Not Found"


def test_post_barrio(tangaras):
    id_comuna = random.choice(range(
        Codes.COMUNA, 
        Codes.COMUNA + Totals.COMUNAS)
    )
    barrio1 = BarrioCreate(
        id=fake.random_int(min=Codes.BARRIO + Totals.BARRIOS + 1, max=Codes.VEREDA), 
        id_comuna=id_comuna, 
        nombre=f"Barrio {fake.unique.street_name()}", 
        codigo=f"{fake.unique.bothify(text='???_###').upper()}", 
        estrato=f"{fake.random_int(min=0, max=9)}"
    )
    response1 = client.post(f"/barrios/", json=barrio1.dict())

    barrio2 = barrio1.copy()
    response2 = client.post(f"/barrios/", json=barrio2.dict())

    barrio3 = barrio1.copy()
    barrio3.id = barrio1.id + 1
    response3 = client.post(f"/barrios/", json=barrio3.dict())

    assert response1.status_code == status.HTTP_201_CREATED
    assert barrio1.id == BarrioSchema.validate(response1.json()).id
    assert response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response2.json()["detail"] == "Barrio id must be Unique"
    assert response3.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response3.json()["detail"] == "Barrio codigo must be Unique"


def test_put_barrio(tangaras):
    id_barrio = random.choice(range(
        Codes.BARRIO,
        Codes.BARRIO + Totals.BARRIOS)
    )
    response1 = client.get(f"/barrios/{id_barrio}")
    barrio1 = response1.json()
    barrio1 = BarrioSchema.validate(barrio1)

    id_comuna = random.choice(range(
        Codes.COMUNA, 
        Codes.COMUNA + Totals.COMUNAS)
    )

    barrio1.id_comuna = id_comuna
    barrio1.nombre = f"Barrio {fake.unique.street_name()}"
    barrio1.codigo = f"{fake.unique.bothify(text='???_###').upper()}"
    barrio1.estrato = f"{fake.random_int(min=0, max=9)}"

    response2 = client.put(f"/barrios/{id_barrio}", json=barrio1.dict())
    barrio2 = response2.json()
    barrio2 = BarrioSchema.validate(barrio2)


    assert response1.status_code == status.HTTP_200_OK
    assert barrio1.id == id_barrio
    assert response2.status_code == status.HTTP_200_OK
    assert barrio2.id == barrio1.id
    assert barrio2.id_comuna == barrio1.id_comuna
    assert barrio2.nombre == barrio1.nombre
    assert barrio2.codigo == barrio1.codigo
    assert barrio2.estrato == barrio1.estrato


def test_delete_barrio(tangaras):
    id_barrio = random.choice(range(
        Codes.BARRIO,
        Codes.BARRIO + Totals.BARRIOS)
    )
    response1 = client.delete(f"/barrios/{id_barrio}")

    response2 = client.get(f"/barrios/{id_barrio}")

    assert response1.status_code == status.HTTP_204_NO_CONTENT
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert response2.json()["detail"] == "Not Found"


def test_get_tangaras(tangaras):
    id_barrio = random.choice(range(
        Codes.BARRIO,
        Codes.BARRIO + Totals.BARRIOS)
    )
    response = client.get(f"/barrios/{id_barrio}/tangaras")
    tangaras = response.json()
    TangaraSchemaList.validate({"tangaras": tangaras})
    # print("tangaras:", tangaras)

    assert response.status_code == status.HTTP_200_OK
