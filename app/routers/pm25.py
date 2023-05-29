from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from enum import IntEnum

from app.dependencies.database import get_db
from app.schemas.lugares import LugaresSchema
from app.schemas.tangara import TangaraSchemaList
from app.schemas.pm25 import PM25Schema
from app.crud.comuna import ComunaCRUD
from app.crud.barrio import BarrioCRUD
from app.crud.vereda import VeredaCRUD
from app.crud.sector import SectorCRUD
from app.crud.areaexp import AreaExpCRUD
from app.crud.areapro import AreaProCRUD


# IDs Lugares
class Codes(IntEnum):
    COMUNA = 1000
    BARRIO = 2000
    VEREDA = 3000
    SECTOR = 4000
    AREAEXP = 5000
    AREAPRO = 6000


router = APIRouter(
    prefix="/pm25",
    tags=["pm25"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=PM25Schema, status_code=status.HTTP_200_OK)
async def realtime(lugar: LugaresSchema, db: Session = Depends(get_db)) -> PM25Schema:
    
    tangaras = []

    if lugar.id in range(Codes.COMUNA, Codes.BARRIO):
        tangaras = ComunaCRUD.read_tangaras(db, id_comuna=lugar.id)
    if lugar.id in range(Codes.BARRIO, Codes.VEREDA):
        tangaras = BarrioCRUD.read_tangaras(db, id_barrio=lugar.id)
    if lugar.id in range(Codes.VEREDA, Codes.SECTOR):
        tangaras = VeredaCRUD.read_tangaras(db, id_vereda=lugar.id)
    if lugar.id in range(Codes.SECTOR, Codes.AREAEXP):
        tangaras = SectorCRUD.read_tangaras(db, id_sector=lugar.id)
    if lugar.id in range(Codes.AREAEXP, Codes.AREAPRO):
        tangaras = AreaExpCRUD.read_tangaras(db, id_areaexp=lugar.id)
    if lugar.id in range(Codes.AREAPRO, Codes.AREAPRO + 1000):
        tangaras = AreaProCRUD.read_tangaras(db, id_areapro=lugar.id)

    print(tangaras)

    pm25_realtime = PM25Schema(pm25=12.4, aqi=30, aqi_color="Green", aqi_category="Healthy", aqi_desc="Healthy day", datetime="now")
    
    return pm25_realtime
