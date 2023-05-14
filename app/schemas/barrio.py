from pydantic import BaseModel

from datetime import datetime, timezone, timedelta


class BarrioBase(BaseModel):
    nombre: str
    codigo: str
    estrato: str


class BarrioCreate(BarrioBase):
    created: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class BarrioUpdate(BarrioBase):
    updated: str = datetime.now(tz=timezone(
        offset=-timedelta(hours=5), name='America/Bogota')).isoformat()


class Barrio(BarrioBase):
    id: int
    id_comuna: int
    comuna: "Comuna"  # type: ignore
    tangaras: list["Tangara"] = []  # type: ignore

    class Config:
        orm_mode = True
