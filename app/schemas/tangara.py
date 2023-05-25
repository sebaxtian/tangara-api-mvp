from pydantic import BaseModel
from datetime import datetime, timezone, timedelta


class TangaraBase(BaseModel):
    mac: str
    geohash: str
    codigo: str
    latitud: str
    longitud: str
    online: bool = False
    id_barrio: int | None
    id_sector: int | None
    id_areaexp: int | None
    id_areapro: int | None


class TangaraCreate(TangaraBase):
    id: int | None
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


class TangaraSchemaList(BaseModel):
    tangaras: list[TangaraSchema]
