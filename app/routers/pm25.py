from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from enum import IntEnum

from app.dependencies.database import get_db
from app.schemas.tangara import TangaraSchema
from app.schemas.pm25 import PM25Schema
from app.crud.comuna import ComunaCRUD
from app.crud.barrio import BarrioCRUD
from app.crud.vereda import VeredaCRUD
from app.crud.sector import SectorCRUD
from app.crud.areaexp import AreaExpCRUD
from app.crud.areapro import AreaProCRUD
from app.utils.pm25 import pm25_realtime


# IDs Lugares
class Codes(IntEnum): #TODO: Refactoring
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


@router.get("/{id}", response_model=PM25Schema, status_code=status.HTTP_200_OK)
async def realtime(id: int, db: Session = Depends(get_db)) -> PM25Schema:
    
    tangaras: list[TangaraSchema] = []

    if id in range(Codes.COMUNA, Codes.BARRIO):
        tangaras = ComunaCRUD.read_tangaras(db, id_comuna=id)
    if id in range(Codes.BARRIO, Codes.VEREDA):
        tangaras = BarrioCRUD.read_tangaras(db, id_barrio=id)
    if id in range(Codes.VEREDA, Codes.SECTOR):
        tangaras = VeredaCRUD.read_tangaras(db, id_vereda=id)
    if id in range(Codes.SECTOR, Codes.AREAEXP):
        tangaras = SectorCRUD.read_tangaras(db, id_sector=id)
    if id in range(Codes.AREAEXP, Codes.AREAPRO):
        tangaras = AreaExpCRUD.read_tangaras(db, id_areaexp=id)
    if id in range(Codes.AREAPRO, Codes.AREAPRO + 1000):
        tangaras = AreaProCRUD.read_tangaras(db, id_areapro=id)

    mac_addresses: list[str] = [tangara.mac for tangara in tangaras]
    # Check data
    if len(mac_addresses) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tangaras Not Found")
    
    return await pm25_realtime(mac_addresses)