from pydantic import BaseModel

from datetime import datetime, timezone, timedelta

from ..models.sector import Sector


class VeredaBase(BaseModel):
    nombre: str
    codigo: str


class VeredaCreate(VeredaBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class VeredaUpdate(VeredaBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class Vereda(VeredaBase):
    id: int
    sectores: list[Sector] = []

    class Config:
        orm_mode = True
