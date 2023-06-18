from pydantic import BaseModel
from datetime import datetime, timezone, timedelta

from app.schemas.tangara import TangaraSchema


class AreaProBase(BaseModel):
    nombre: str
    codigo: str


class AreaProCreate(AreaProBase):
    id: int | None
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()
    updated: str = created


class AreaProUpdate(AreaProBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class AreaProSchema(AreaProBase):
    id: int
    tangaras: list[TangaraSchema]
    created: str
    updated: str

    class Config:
        orm_mode = True


class AreaProPaginationSchema(BaseModel):
    count: int
    skip: int
    limit: int
    areaspro: list[AreaProSchema]
