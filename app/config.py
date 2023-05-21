from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tangara API MVP"
    env: str

    class Config:
        env_file = "app/.env"
