from pydantic import BaseModel
from datetime import datetime, timezone, timedelta

from app.schemas.barrio import BarrioSchema


class ComunaBase(BaseModel):
    nombre: str
    codigo: str


class ComunaCreate(ComunaBase):
    id: int | None
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()
    updated: str = created


class ComunaUpdate(ComunaBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class ComunaSchema(ComunaBase):
    id: int
    barrios: list[BarrioSchema]
    created: str
    updated: str

    class Config:
        orm_mode = True


class ComunaPaginationSchema(BaseModel):
    count: int
    skip: int
    limit: int
    comunas: list[ComunaSchema]
