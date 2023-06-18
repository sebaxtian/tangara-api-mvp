from fastapi.testclient import TestClient
from fastapi import status
import pandas as pd
import io

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db
from app.tests.conftest import Codes


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_lugares(tangaras):
    codes = [Codes.COMUNA, Codes.BARRIO, Codes.VEREDA, Codes.SECTOR, Codes.AREAEXP, Codes.AREAPRO]
    
    response1 = client.get("/lugares/")
    lugares = response1.json()

    df_lugares = pd.DataFrame(data=lugares)
    ids_lugares = df_lugares['id'].astype('int').values
    # print(ids_lugares)

    response2 = client.get("/lugares/?format=csv")
    lugares_csv = response2.content
    if len(lugares_csv) > 1:
        df_lugares_csv = pd.read_csv(io.BytesIO(lugares_csv))
        ids_lugares_csv = df_lugares_csv['id'].astype('int').values
        assert all(code in ids_lugares_csv for code in codes) == True
    # print(ids_lugares_csv)

    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK
    assert all(code in ids_lugares for code in codes) == True
