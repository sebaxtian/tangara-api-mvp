from pydantic import BaseModel

from datetime import datetime, timezone, timedelta

from ..models.barrio import Barrio
from ..models.sector import Sector
from ..models.areaexp import AreaExp
from ..models.areapro import AreaPro


class TangaraBase(BaseModel):
    mac: str
    geohash: str
    codigo: str
    latitud: str
    longitud: str
    online: bool = False


class TangaraCreate(TangaraBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class TangaraUpdate(TangaraBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class Tangara(TangaraBase):
    id: int
    id_barrio: int
    id_sector: int
    id_areaexp: int
    id_areapro: int

    barrio: Barrio
    sector: Sector
    areaexp: AreaExp
    areapro: AreaPro

    class Config:
        orm_mode = True
