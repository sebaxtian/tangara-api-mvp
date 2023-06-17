from pydantic import BaseModel
from datetime import datetime, timezone, timedelta

from app.schemas.tangara import TangaraSchema


class BarrioBase(BaseModel):
    id_comuna: int
    nombre: str
    codigo: str
    estrato: str


class BarrioCreate(BarrioBase):
    id: int | None
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

# TODO: Remove Method, replaced by BarrioPaginationSchema
class BarrioSchemaList(BaseModel):
    barrios: list[BarrioSchema]


class BarrioPaginationSchema(BaseModel):
    count: int
    skip: int
    limit: int
    barrios: list[BarrioSchema]
