from fastapi.testclient import TestClient
from fastapi import status
import random
from faker import Faker

# import pytest
# from httpx import AsyncClient
"""
@pytest.mark.anyio
async def test_comunas(comunas):
    async with AsyncClient(app=app, base_url="http://tests") as ac:
        response = await ac.get("/comunas/")

    print("response.json()", response.json())
    assert response.status_code == 200
"""

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Totals, Codes

from app.schemas.comuna import ComunaPaginationSchema, ComunaSchema, ComunaCreate
from app.schemas.barrio import BarrioPaginationSchema
from app.schemas.tangara import TangaraPaginationSchema


fake = Faker()
fake.seed_instance('tangara-mvp')


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_comunas(tangaras):
    response = client.get("/comunas/")
    comunas = response.json()
    comunas = ComunaPaginationSchema.validate(comunas)
    # print("comunas:", comunas)

    assert response.status_code == status.HTTP_200_OK
    assert comunas.count == Totals.COMUNAS


def test_get_comunas_pagination(tangaras):
    response_page1 = client.get(f"/comunas/?limit={round(Totals.COMUNAS / 2)}&skip=0")
    comunas_page1 = response_page1.json()
    comunas_page1 = ComunaPaginationSchema.validate(comunas_page1)

    response_page2 = client.get(f"/comunas/?limit={round(Totals.COMUNAS / 2)}&skip={round(Totals.COMUNAS / 2)}")
    comunas_page2 = response_page2.json()
    comunas_page2 = ComunaPaginationSchema.validate(comunas_page2)

    response_page3 = client.get(f"/comunas/?limit={Totals.COMUNAS}&skip={Totals.COMUNAS}")
    comunas_page3 = response_page3.json()
    comunas_page3 = ComunaPaginationSchema.validate(comunas_page3)

    assert response_page1.status_code == status.HTTP_200_OK
    assert response_page2.status_code == status.HTTP_200_OK
    assert response_page3.status_code == status.HTTP_200_OK
    assert comunas_page1.count == round(Totals.COMUNAS / 2)
    assert comunas_page1.count + comunas_page2.count == Totals.COMUNAS
    assert comunas_page3.count == 0


def test_get_comuna_by_id(tangaras):
    id_comuna = random.choice(range(
        Codes.COMUNA,
        Codes.COMUNA + Totals.COMUNAS)
    )
    response_found = client.get(f"/comunas/{id_comuna}")
    comuna_found = response_found.json()
    comuna_found = ComunaSchema.validate(comuna_found)
    # print("comuna_found:", comuna_found)

    response_not_found = client.get(f"/comunas/{Codes.BARRIO}")
    comuna_not_found = response_not_found.json()

    assert response_found.status_code == status.HTTP_200_OK
    assert comuna_found.id == id_comuna
    assert response_not_found.status_code == status.HTTP_404_NOT_FOUND
    assert comuna_not_found["detail"] == "Comuna not found"


def test_post_comuna(tangaras):
    comuna1 = ComunaCreate(
        id=fake.random_int(min=Codes.COMUNA + Totals.COMUNAS + 1, max=Codes.BARRIO), 
        nombre=f"Comuna {fake.unique.bothify(text='###')}", 
        codigo=f"{fake.unique.bothify(text='???_###').upper()}"
    )
    response1 = client.post(f"/comunas/", json=comuna1.dict())

    comuna2 = comuna1.copy()
    response2 = client.post(f"/comunas/", json=comuna2.dict())

    comuna3 = comuna1.copy()
    comuna3.id = comuna1.id + 1
    response3 = client.post(f"/comunas/", json=comuna3.dict())

    assert response1.status_code == status.HTTP_201_CREATED
    assert comuna1.id == ComunaSchema.validate(response1.json()).id
    assert response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response2.json()["detail"] == "Comuna id must be Unique"
    assert response3.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response3.json()["detail"] == "Comuna codigo must be Unique"


def test_put_comuna(tangaras):
    id_comuna = random.choice(range(
        Codes.COMUNA,
        Codes.COMUNA + Totals.COMUNAS)
    )
    response1 = client.get(f"/comunas/{id_comuna}")
    comuna1 = response1.json()
    comuna1 = ComunaSchema.validate(comuna1)

    comuna1.nombre = f"Comuna {fake.unique.bothify(text='###')}"
    comuna1.codigo = f"{fake.unique.bothify(text='???_###').upper()}"

    response2 = client.put(f"/comunas/{id_comuna}", json=comuna1.dict())
    comuna2 = response2.json()
    comuna2 = ComunaSchema.validate(comuna2)

    response1 = client.get(f"/comunas/{id_comuna}")
    comuna1 = response1.json()
    comuna1 = ComunaSchema.validate(comuna1)

    assert response1.status_code == status.HTTP_200_OK
    assert comuna1.id == id_comuna
    assert response2.status_code == status.HTTP_200_OK
    assert comuna2.id == comuna1.id
    assert comuna2.nombre == comuna1.nombre
    assert comuna2.codigo == comuna1.codigo


def test_delete_comuna(tangaras):
    id_comuna = random.choice(range(
        Codes.COMUNA,
        Codes.COMUNA + Totals.COMUNAS)
    )
    response1 = client.delete(f"/comunas/{id_comuna}")

    response2 = client.get(f"/comunas/{id_comuna}")

    assert response1.status_code == status.HTTP_204_NO_CONTENT
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    assert response2.json()["detail"] == "Comuna not found"


def test_get_comunas_barrios(tangaras):
    id_comuna = random.choice(range(
        Codes.COMUNA,
        Codes.COMUNA + Totals.COMUNAS)
    )
    response = client.get(f"/comunas/{id_comuna}/barrios")
    barrios = response.json()
    BarrioPaginationSchema.validate(barrios)
    # print("barrios:", barrios)

    assert response.status_code == status.HTTP_200_OK


def test_get_comunas_tangaras(tangaras):
    id_comuna = random.choice(range(
        Codes.COMUNA,
        Codes.COMUNA + Totals.COMUNAS)
    )
    response = client.get(f"/comunas/{id_comuna}/tangaras")
    tangaras = response.json()
    TangaraPaginationSchema.validate(tangaras)
    # print("tangaras:", tangaras)

    assert response.status_code == status.HTTP_200_OK
