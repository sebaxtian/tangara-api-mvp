from pydantic import BaseModel

from datetime import datetime, timezone, timedelta

from ..models.vereda import Vereda
from ..models.tangara import Tangara


class SectorBase(BaseModel):
    nombre: str
    codigo: str


class SectorCreate(SectorBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class SectorUpdate(SectorBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class Sector(SectorBase):
    id: int
    id_vereda: int
    vereda: Vereda
    tangaras: list[Tangara] = []

    class Config:
        orm_mode = True
