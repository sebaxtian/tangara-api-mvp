from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tangara API MVP"
    env: str
    url_influxdb: str
    db_influxdb: str
    url_redis: str

    class Config:
        env_file = "app/.env"
