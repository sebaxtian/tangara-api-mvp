from pydantic import BaseModel

from datetime import datetime, timezone, timedelta


class ComunaBase(BaseModel):
    nombre: str
    codigo: str


class ComunaCreate(ComunaBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()
    updated: str = created


class ComunaUpdate(ComunaBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class Comuna(ComunaBase):
    id: int
    barrios: list["Barrio"] = [] # type: ignore
    created: str
    updated: str

    class Config:
        orm_mode = True
