from pydantic import BaseModel


class PM25Schema(BaseModel):
    pm25: float
    aqi: int
    aqi_color: str
    aqi_category: str
    aqi_desc: str
    datetime: str


class TimeSeriesSchema(BaseModel):
    timeseries: list[PM25Schema]
