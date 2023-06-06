from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tangara API MVP"
    env: str
    url_influxdb: str
    db_influxdb: str
    redis_server: str

    class Config:
        env_file = "app/.env"
