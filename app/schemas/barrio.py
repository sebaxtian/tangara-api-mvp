from pydantic import BaseModel
from datetime import datetime, timezone, timedelta

from app.schemas.tangara import TangaraSchema


class BarrioBase(BaseModel):
    id_comuna: int
    nombre: str
    codigo: str
    estrato: str


class BarrioCreate(BarrioBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()
    updated: str = created


class BarrioUpdate(BarrioBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class BarrioSchema(BarrioBase):
    id: int
    tangaras: list[TangaraSchema]
    created: str
    updated: str

    class Config:
        orm_mode = True
