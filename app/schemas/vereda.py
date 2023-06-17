from pydantic import BaseModel
from datetime import datetime, timezone, timedelta

from app.schemas.sector import SectorSchema


class VeredaBase(BaseModel):
    nombre: str
    codigo: str


class VeredaCreate(VeredaBase):
    id: int | None
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()
    updated: str = created


class VeredaUpdate(VeredaBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class VeredaSchema(VeredaBase):
    id: int
    sectores: list[SectorSchema]
    created: str
    updated: str

    class Config:
        orm_mode = True


class VeredaPaginationSchema(BaseModel):
    count: int
    skip: int
    limit: int
    veredas: list[VeredaSchema]
