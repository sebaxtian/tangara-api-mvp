from fastapi.testclient import TestClient

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

from app.tests.conftest import Totals
from app.dependencies.testing_database import override_get_db
from app.main import app, get_db

from app.schemas.comuna import ComunaSchemaList
from app.schemas.barrio import BarrioSchemaList
from app.schemas.vereda import VeredaSchemaList
from app.schemas.sector import SectorSchemaList
from app.schemas.areaexp import AreaExpSchemaList
from app.schemas.areapro import AreaProSchemaList
from app.schemas.tangara import TangaraSchemaList

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

from typing import List

def test_comunas(tangaras):
    response = client.get("/comunas/")
    comunas = response.json()
    ComunaSchemaList.validate({"comunas": comunas})
    #print("comunas:", comunas)

    assert response.status_code == 200
    assert len(comunas) == Totals.COMUNAS


def test_barrios(tangaras):
    response = client.get("/barrios/")
    barrios = response.json()
    BarrioSchemaList.validate({"barrios": barrios})
    #print("barrios:", barrios)

    assert response.status_code == 200
    assert len(barrios) == Totals.BARRIOS


def test_veredas(tangaras):
    response = client.get("/veredas/")
    veredas = response.json()
    VeredaSchemaList.validate({"veredas": veredas})
    #print("veredas:", veredas)

    assert response.status_code == 200
    assert len(veredas) == Totals.VEREDAS


def test_sectores(tangaras):
    response = client.get("/sectores/")
    sectores = response.json()
    SectorSchemaList.validate({"sectores": sectores})
    #print("sectores:", sectores)

    assert response.status_code == 200
    assert len(sectores) == Totals.SECTORES


def test_areasexp(tangaras):
    response = client.get("/areasexp/")
    areasexp = response.json()
    AreaExpSchemaList.validate({"areasexp": areasexp})
    #print("areasexp:", areasexp)

    assert response.status_code == 200
    assert len(areasexp) == Totals.AREASEXP


def test_areaspro(tangaras):
    response = client.get("/areaspro/")
    areaspro = response.json()
    AreaProSchemaList.validate({"areaspro": areaspro})
    #print("areaspro:", areaspro)

    assert response.status_code == 200
    assert len(areaspro) == Totals.AREASPRO


def test_tangaras(tangaras):
    response = client.get("/tangaras/")
    tangaras = response.json()
    TangaraSchemaList.validate({"tangaras": tangaras})
    #print("tangaras:", tangaras)

    assert response.status_code == 200
    assert len(tangaras) == Totals.TANGARAS
