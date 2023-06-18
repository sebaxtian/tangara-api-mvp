from pydantic import BaseModel
from datetime import datetime, timezone, timedelta

from app.schemas.tangara import TangaraSchema


class AreaExpBase(BaseModel):
    nombre: str
    codigo: str


class AreaExpCreate(AreaExpBase):
    id: int | None
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()
    updated: str = created


class AreaExpUpdate(AreaExpBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class AreaExpSchema(AreaExpBase):
    id: int
    tangaras: list[TangaraSchema]
    created: str
    updated: str

    class Config:
        orm_mode = True


class AreaExpPaginationSchema(BaseModel):
    count: int
    skip: int
    limit: int
    areasexp: list[AreaExpSchema]
