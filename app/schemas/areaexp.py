from pydantic import BaseModel

from datetime import datetime, timezone, timedelta

from ..models.tangara import Tangara


class AreaExpBase(BaseModel):
    nombre: str
    codigo: str


class AreaExpCreate(AreaExpBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class AreaExpUpdate(AreaExpBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class AreaExp(AreaExpBase):
    id: int
    tangaras: list[Tangara] = []

    class Config:
        orm_mode = True
