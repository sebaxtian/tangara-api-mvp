from fastapi.testclient import TestClient
from fastapi import status
import pandas as pd
import random
from faker import Faker

from app.main import app, get_db
from app.dependencies.testing_database import override_get_db

from app.schemas.pm25 import PM25Schema, TimeSeriesSchema


fake = Faker()
fake.seed_instance('tangara-mvp')


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_realtime(pm25):
    response = client.get("/lugares/")
    lugares = response.json()

    df_lugares = pd.DataFrame(data=lugares)
    ids_lugares = df_lugares['id'].astype('int').values
    id_lugar = random.choice(ids_lugares)

    response = client.get(f"/pm25/{id_lugar}")
    #print("response.json():", response.json())
    pm25realtime = response.json()
    #print("pm25realtime:", pm25realtime)

    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert pm25realtime['detail'] in ["Tangaras Data Not Found", "Tangaras Not Found"]
    else:
        assert response.status_code == status.HTTP_200_OK
        pm25realtime = PM25Schema.validate(pm25realtime)
        assert pm25realtime.pm25 >= 0
        assert pm25realtime.aqi >= 0
        assert pm25realtime.aqi_color in ['#00e400', '#ffff00', '#ff7e00', '#ff0000', '#8f3f97', '#7e0023']
        assert pm25realtime.aqi_category in ['Good', 'Moderate', 'Unhealthy for sensitive groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
        assert pm25realtime.aqi_desc in [
            'Air quality is satisfactory, and air pollution poses little or no risk.', 
            'Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.', 
            'Members of sensitive groups may experience health effects. The general public is less likely to be affected.', 
            'Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.', 
            'Health alert: The risk of health effects is increased for everyone.', 
            'Health warning of emergency conditions: everyone is more likely to be affected.'
        ]


def test_get_last_1_hour(pm25):
    response = client.get("/lugares/")
    lugares = response.json()

    df_lugares = pd.DataFrame(data=lugares)
    ids_lugares = df_lugares['id'].astype('int').values
    id_lugar = random.choice(ids_lugares)

    response = client.get(f"/pm25/last1h/{id_lugar}")
    #print("response.json():", response.json())
    pm25last1h = response.json()
    #print("pm25last1h:", pm25last1h)

    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert pm25last1h['detail'] in ["Tangaras Data Not Found", "Tangaras Not Found"]
    else:
        assert response.status_code == status.HTTP_200_OK
        pm25last1h = PM25Schema.validate(pm25last1h)
        assert pm25last1h.pm25 >= 0
        assert pm25last1h.aqi >= 0
        assert pm25last1h.aqi_color in ['#00e400', '#ffff00', '#ff7e00', '#ff0000', '#8f3f97', '#7e0023']
        assert pm25last1h.aqi_category in ['Good', 'Moderate', 'Unhealthy for sensitive groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
        assert pm25last1h.aqi_desc in [
            'Air quality is satisfactory, and air pollution poses little or no risk.', 
            'Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.', 
            'Members of sensitive groups may experience health effects. The general public is less likely to be affected.', 
            'Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.', 
            'Health alert: The risk of health effects is increased for everyone.', 
            'Health warning of emergency conditions: everyone is more likely to be affected.'
        ]


def test_get_last_24_hours(pm25):
    response = client.get("/lugares/")
    lugares = response.json()

    df_lugares = pd.DataFrame(data=lugares)
    ids_lugares = df_lugares['id'].astype('int').values
    id_lugar = random.choice(ids_lugares)

    response = client.get(f"/pm25/last24h/{id_lugar}")
    #print("response.json():", response.json())
    pm25last24h = response.json()
    #print("pm25last24h:", pm25last24h)

    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert pm25last24h['detail'] in ["Tangaras Data Not Found", "Tangaras Not Found"]
    else:
        assert response.status_code == status.HTTP_200_OK
        pm25last24h = PM25Schema.validate(pm25last24h)
        assert pm25last24h.pm25 >= 0
        assert pm25last24h.aqi >= 0
        assert pm25last24h.aqi_color in ['#00e400', '#ffff00', '#ff7e00', '#ff0000', '#8f3f97', '#7e0023']
        assert pm25last24h.aqi_category in ['Good', 'Moderate', 'Unhealthy for sensitive groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
        assert pm25last24h.aqi_desc in [
            'Air quality is satisfactory, and air pollution poses little or no risk.', 
            'Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.', 
            'Members of sensitive groups may experience health effects. The general public is less likely to be affected.', 
            'Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.', 
            'Health alert: The risk of health effects is increased for everyone.', 
            'Health warning of emergency conditions: everyone is more likely to be affected.'
        ]


def test_get_movil_24_hours(pm25):
    response = client.get("/lugares/")
    lugares = response.json()

    df_lugares = pd.DataFrame(data=lugares)
    ids_lugares = df_lugares['id'].astype('int').values
    id_lugar = random.choice(ids_lugares)

    response = client.get(f"/pm25/movil24h/{id_lugar}")
    #print("response.json():", response.json())
    pm25movil24h = response.json()
    #print("pm25movil24h:", pm25movil24h)

    if response.status_code == status.HTTP_404_NOT_FOUND:
        assert pm25movil24h['detail'] in ["Tangaras Data Not Found", "Tangaras Not Found"]
    else:
        assert response.status_code == status.HTTP_200_OK
        pm25movil24h = TimeSeriesSchema.validate({"timeseries": pm25movil24h}).timeseries
        assert len(pm25movil24h) == 25
        assert pm25movil24h[0].pm25 >= 0
        assert pm25movil24h[0].aqi >= 0
        assert pm25movil24h[0].aqi_color in ['#00e400', '#ffff00', '#ff7e00', '#ff0000', '#8f3f97', '#7e0023']
        assert pm25movil24h[0].aqi_category in ['Good', 'Moderate', 'Unhealthy for sensitive groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
        assert pm25movil24h[0].aqi_desc in [
            'Air quality is satisfactory, and air pollution poses little or no risk.', 
            'Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.', 
            'Members of sensitive groups may experience health effects. The general public is less likely to be affected.', 
            'Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.', 
            'Health alert: The risk of health effects is increased for everyone.', 
            'Health warning of emergency conditions: everyone is more likely to be affected.'
        ]
