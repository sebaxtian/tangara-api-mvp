from pydantic import BaseModel

from datetime import datetime, timezone, timedelta

from ..models.tangara import Tangara


class AreaProBase(BaseModel):
    nombre: str
    codigo: str


class AreaProCreate(AreaProBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class AreaProUpdate(AreaProBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class AreaPro(AreaProBase):
    id: int
    tangaras: list[Tangara] = []

    class Config:
        orm_mode = True
