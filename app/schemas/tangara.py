from pydantic import BaseModel
from datetime import datetime, timezone, timedelta


class TangaraBase(BaseModel):
    mac: str
    geohash: str
    codigo: str
    latitud: str
    longitud: str
    online: bool
    id_areaexp: int


class TangaraCreate(TangaraBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()
    updated: str = created


class TangaraUpdate(TangaraBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class TangaraSchema(TangaraBase):
    id: int
    created: str
    updated: str

    class Config:
        orm_mode = True
