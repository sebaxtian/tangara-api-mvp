from pydantic import BaseModel
from datetime import datetime, timezone, timedelta

from app.schemas.tangara import TangaraSchema


class SectorBase(BaseModel):
    id_vereda: int
    nombre: str
    codigo: str


class SectorCreate(SectorBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()
    updated: str = created


class SectorUpdate(SectorBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class SectorSchema(SectorBase):
    id: int
    tangaras: list[TangaraSchema]
    created: str
    updated: str

    class Config:
        orm_mode = True
