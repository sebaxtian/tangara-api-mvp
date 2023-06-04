import math, sys
import pandas as pd
from fastapi import HTTPException, status
from io import StringIO
from requests import get as GET, Response
from datetime import datetime, timezone, timedelta
from typing import List

from app.config import Settings
from app.dependencies.settings import get_settings

from app.schemas.pm25 import PM25Schema


settings: Settings = get_settings()


# Request to InfluxDB API REST
def request_influxdb(sql_query: str) -> Response:
    endpoint = settings.url_influxdb
    database = settings.db_influxdb
    parameters = {
        'db': database,
        'q': sql_query,
        'epoch': 'ms'
    }
    # To get response as CSV text
    headers = {'Accept': 'application/csv'}
    # GET Request
    return GET(endpoint, params=parameters, headers=headers)


# Read documentation: notebooks/pm25_to_aqi.ipynb
class PM25_TO_AQI(): #TODO: Refactoring
    # Levels of Concern
    GOOD = 0
    MODERATE = 1
    UNHEALTHY_FOR_SENSITIVE_GROUPS = 2
    UNHEALTHY = 3
    VERY_UNHEALTHY = 4
    HAZARDOUS = 5
    # AQI Levels
    AQI_LEVELS = (
        (GOOD, 'Good', [0, 50]), # 0 - 50
        (MODERATE, 'Moderate', [51, 100]), # 51 - 100
        (UNHEALTHY_FOR_SENSITIVE_GROUPS, 'Unhealthy for sensitive groups', [101, 150]), # 101 - 150
        (UNHEALTHY, 'Unhealthy', [151, 200]), # 151 - 200
        (VERY_UNHEALTHY, 'Very Unhealthy', [201, 300]), # 201 - 300
        (HAZARDOUS, 'Hazardous', [301, sys.maxsize]), # 301 - higher
    )
    # PM25 Breakpoints Values
    PM25_BREAKPOINTS = (
        (GOOD, 'Good', [0.0, 12.0]), # 0.0 - 12.0, Good
        (MODERATE, 'Moderate', [12.1, 35.4]), # 12.1 - 35.4, Moderate
        (UNHEALTHY_FOR_SENSITIVE_GROUPS, 'Unhealthy for sensitive groups', [35.5, 55.4]), # 35.5 - 55.4, Unhealthy for sensitive groups
        (UNHEALTHY, 'Unhealthy', [55.5, 150.4]), # 55.5 - 150.4, Unhealthy
        (VERY_UNHEALTHY, 'Very Unhealthy', [150.5, 250.4]), # 150.5 - 250.4, Very Unhealthy
        (HAZARDOUS, 'Hazardous', [250.5, 350.4]), # 250.5 - 350.4, Hazardous
        (HAZARDOUS, 'Hazardous', [350.5, 500.4]), # 350.5 - 500.4, Hazardous
    )
    # Max PM25 Value
    MAX_PM25_VALUE = 500.5

    def aqi_color(self, aqi_value: int) -> str:
        # Green
        if aqi_value in range(0, 51):
            return '#00e400'
        # Yellow
        if aqi_value in range(51, 101):
            return '#ffff00'
        # Orange
        if aqi_value in range(101, 151):
            return '#ff7e00'
        # Red
        if aqi_value in range(151, 201):
            return '#ff0000'
        # Purple
        if aqi_value in range(201, 301):
            return '#8f3f97'
        # aqi_value in range(301, sys.maxsize)
        # Maroon
        return '#7e0023'
    
    def aqi_category(self, aqi_value: int) -> str:
        # Green
        if aqi_value in range(0, 51):
            return 'Good'
        # Yellow
        if aqi_value in range(51, 101):
            return 'Moderate'
        # Orange
        if aqi_value in range(101, 151):
            return 'Unhealthy for sensitive groups'
        # Red
        if aqi_value in range(151, 201):
            return 'Unhealthy'
        # Purple
        if aqi_value in range(201, 301):
            return 'Very Unhealthy'
        # aqi_value in range(301, sys.maxsize)
        # Maroon
        return 'Hazardous'
    
    def aqi_desc(self, aqi_value: int) -> str:
        # Green
        if aqi_value in range(0, 51):
            return 'Air quality is satisfactory, and air pollution poses little or no risk.'
        # Yellow
        if aqi_value in range(51, 101):
            return 'Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.'
        # Orange
        if aqi_value in range(101, 151):
            return 'Members of sensitive groups may experience health effects. The general public is less likely to be affected.'
        # Red
        if aqi_value in range(151, 201):
            return 'Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.'
        # Purple
        if aqi_value in range(201, 301):
            return 'Health alert: The risk of health effects is increased for everyone.'
        # aqi_value in range(301, sys.maxsize)
        # Maroon
        return 'Health warning of emergency conditions: everyone is more likely to be affected.'
    # Define Equation 1 to Calculate AQI Value
    #
    # AQI = AQI for pollutant p
    # Cp = The truncated concentrattion of pollutant p
    # BP_hi = The concentration breakpoint that is greater than or equal to Cp
    # BP_lo = The concentration breakpoint that is less than or equal to Cp
    # AQI_hi = The AQI value corresponding to BP_hi
    # AQI_lo = The AQI value corresponding to BP_lo
    #
    def equation1(self, Cp: float) -> int:
        # Truncate Cp
        Cp = float(f'{Cp:.1f}')
        # AQI Value to Concentration of Pollutant P
        AQI = None
        # Variables
        BP_hi = None
        BP_lo = None
        AQI_hi = None
        AQI_lo = None

        # Get BP_hi and BP_lo
        for bp in self.PM25_BREAKPOINTS:
            if (Cp >= bp[2][0]) and (Cp <= bp[2][-1]):
                BP_hi = bp[2][-1]
                BP_lo = bp[2][0]
                AQI_hi = self.AQI_LEVELS[bp[0]][2][-1]
                AQI_lo = self.AQI_LEVELS[bp[0]][2][0]
                break

        AQI = Cp if math.isnan(Cp) else math.ceil((((AQI_hi - AQI_lo) / (BP_hi - BP_lo)) * (Cp - BP_lo)) + AQI_lo)

        return AQI


def get_pm25_schema(pm25_value: float, dt_iso_8601: str) -> PM25Schema: #TODO: Refactoring
    aqi_value = PM25_TO_AQI().equation1(pm25_value)
    pm25_schema = PM25Schema(
        pm25=pm25_value, 
        aqi=aqi_value, 
        aqi_color=PM25_TO_AQI().aqi_color(aqi_value), 
        aqi_category=PM25_TO_AQI().aqi_category(aqi_value), 
        aqi_desc=PM25_TO_AQI().aqi_desc(aqi_value), 
        datetime=dt_iso_8601
    )
    return pm25_schema


async def pm25_realtime(mac_addresses: List[str]) -> PM25Schema: #TODO: Refactoring
    # ISO 8601 Format, TZ='America/Bogota' -05:00, Last 5 minutes
    tz_bogota_co = timezone(offset=-timedelta(hours=5), name='America/Bogota')
    time_delta = timedelta(minutes=5)
    # Start DateTime
    start_datetime = (datetime.now(tz=tz_bogota_co) - time_delta).timestamp()
    start_datetime = int(start_datetime) * 1000
    # End DateTime
    end_datetime = datetime.now(tz=tz_bogota_co).timestamp()
    end_datetime = int(end_datetime) * 1000
    # Perdiod DateTime
    period_time = f"time >= {start_datetime}ms AND time <= {end_datetime}ms"
    # SQL Query
    sql_query = f"SELECT mean(\"pm25\") " \
                "FROM \"fixed_stations_01\" WHERE ("
    for mac in mac_addresses:
        sql_query += f"\"name\" = '{mac}' OR "
    sql_query = sql_query[:-4]
    sql_query += f") AND " \
                 f"{period_time} " \
                 f"GROUP BY time(1m) fill(none);"
    # InfluxDB API REST Request
    influxdb_request = request_influxdb(sql_query)
    #print("----->>> influxdb_request.status_code:", influxdb_request.status_code, "influxdb_request.text:", influxdb_request.text)
    if influxdb_request.status_code != status.HTTP_200_OK or not influxdb_request.text:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tangaras Data Not Found")
    # DataFrame last 5 minutes
    df_realtime = pd.read_csv(StringIO(influxdb_request.text), sep=",", low_memory=False)
    # Check data
    if df_realtime.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tangaras Data Not Found")
    # Remove/Add Columns
    df_realtime = df_realtime[['time', 'mean']]
    df_realtime.rename(columns={'time': 'DATETIME', 'mean': 'PM25'}, inplace=True)
    # Date Time ISO 8601 Format, TZ='America/Bogota' -05:00
    df_realtime['DATETIME'] = df_realtime['DATETIME'].apply(lambda x: datetime.fromtimestamp(int(x) / 1000, tz=tz_bogota_co).isoformat())
    # AQI
    #df_realtime['AQI'] = df_realtime['PM25'].apply(lambda x: PM25_TO_AQI.equation1(x))
    #
    #return round(df_realtime['PM25'].mean(), 2)
    return get_pm25_schema(round(df_realtime['PM25'].mean(), 2), datetime.now(tz=tz_bogota_co).isoformat())


async def pm25_last_1_hour(mac_addresses: List[str]) -> PM25Schema: #TODO: Refactoring
    # ISO 8601 Format, TZ='America/Bogota' -05:00, Last 1 hour
    tz_bogota_co = timezone(offset=-timedelta(hours=5), name='America/Bogota')
    time_delta = timedelta(hours=1)
    # Start DateTime
    start_datetime = (datetime.now(tz=tz_bogota_co) - time_delta).timestamp()
    start_datetime = int(start_datetime) * 1000
    # End DateTime
    end_datetime = datetime.now(tz=tz_bogota_co).timestamp()
    end_datetime = int(end_datetime) * 1000
    # Perdiod DateTime
    period_time = f"time >= {start_datetime}ms AND time <= {end_datetime}ms"
    # SQL Query
    sql_query = f"SELECT mean(\"pm25\") " \
                "FROM \"fixed_stations_01\" WHERE ("
    for mac in mac_addresses:
        sql_query += f"\"name\" = '{mac}' OR "
    sql_query = sql_query[:-4]
    sql_query += f") AND " \
                 f"{period_time} " \
                 f"GROUP BY time(1h) fill(none);"
    # InfluxDB API REST Request
    influxdb_request = request_influxdb(sql_query)
    #print("----->>> influxdb_request.status_code:", influxdb_request.status_code, "influxdb_request.text:", influxdb_request.text)
    if influxdb_request.status_code != status.HTTP_200_OK or not influxdb_request.text:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tangaras Data Not Found")
    # DataFrame last 1 hour
    df_last_1_hour = pd.read_csv(StringIO(influxdb_request.text), sep=",", low_memory=False)
    # Check data
    if df_last_1_hour.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tangaras Data Not Found")
    # Remove/Add Columns
    df_last_1_hour = df_last_1_hour[['time', 'mean']]
    df_last_1_hour.rename(columns={'time': 'DATETIME', 'mean': 'PM25'}, inplace=True)
    # Date Time ISO 8601 Format, TZ='America/Bogota' -05:00
    df_last_1_hour['DATETIME'] = df_last_1_hour['DATETIME'].apply(lambda x: datetime.fromtimestamp(int(x) / 1000, tz=tz_bogota_co).isoformat())
    # AQI
    #df_last_1_hour['AQI'] = df_last_1_hour['PM25'].apply(lambda x: PM25_TO_AQI.equation1(x))
    #
    #return round(df_last_1_hour['PM25'].mean(), 2)
    return get_pm25_schema(round(df_last_1_hour['PM25'].mean(), 2), datetime.now(tz=tz_bogota_co).isoformat())
