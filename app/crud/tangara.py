from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.barrio import BarrioModel
from models.tangara import TangaraModel
from schemas.tangara import TangaraSchema, TangaraCreate, TangaraUpdate
from crud.barrio import BarrioCRUD
from crud.sector import SectorCRUD
from crud.areaexp import AreaExpCRUD
from crud.areapro import AreaProCRUD


class TangaraCRUD():

    # Create

    def create_tangara(db: Session, tangara: TangaraCreate) -> TangaraSchema:
        lugares = jsonable_encoder({
            "id_barrio": tangara.id_barrio,
            "id_sector": tangara.id_sector,
            "id_areaexp": tangara.id_areaexp,
            "id_areapro": tangara.id_areapro
        }, exclude_none=True)

        if len(list(lugares.keys())) > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only one accepted: id_barrio, id_sector, id_areaexp, id_areapro")

        if list(lugares.keys())[0] == "id_barrio" and not BarrioCRUD.read_barrio(db, tangara.id_barrio):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Barrio Not Found")
        
        if list(lugares.keys())[0] == "id_sector" and not SectorCRUD.read_sector(db, tangara.id_sector):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Sector Not Found")
        
        if list(lugares.keys())[0] == "id_areaexp" and not AreaExpCRUD.read_areaexp(db, tangara.id_areaexp):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID AreaExp Not Found")
        
        if list(lugares.keys())[0] == "id_areapro" and not AreaProCRUD.read_areapro(db, tangara.id_areapro):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID AreaPro Not Found")
        
        if db.query(TangaraModel).filter(TangaraModel.mac == tangara.mac).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Tangara mac must be Unique")
        
        if db.query(TangaraModel).filter(TangaraModel.codigo == tangara.codigo).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Tangara codigo must be Unique")
        
        tangara = TangaraModel(**tangara.dict())
        db.add(tangara)
        db.commit()
        db.refresh(tangara)
        return tangara

    # Read

    def read_tangaras(db: Session, skip: int = 0, limit: int = 100) -> list[TangaraSchema]:
        return db.query(TangaraModel).offset(skip).limit(limit).all()
    
    def read_tangara(db: Session, id_tangara: int) -> TangaraSchema | None:
        return db.query(TangaraModel).filter(TangaraModel.id == id_tangara).first()

    # Update

    def update_tangara(db: Session, id_tangara: int, tangara: TangaraUpdate) -> TangaraSchema | None:
        lugares = jsonable_encoder({
            "id_barrio": tangara.id_barrio,
            "id_sector": tangara.id_sector,
            "id_areaexp": tangara.id_areaexp,
            "id_areapro": tangara.id_areapro
        }, exclude_none=True)

        if len(list(lugares.keys())) > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only one accepted: id_barrio, id_sector, id_areaexp, id_areapro")

        if list(lugares.keys())[0] == "id_barrio" and not BarrioCRUD.read_barrio(db, tangara.id_barrio):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Barrio Not Found")
        
        if list(lugares.keys())[0] == "id_sector" and not SectorCRUD.read_sector(db, tangara.id_sector):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Sector Not Found")
        
        if list(lugares.keys())[0] == "id_areaexp" and not AreaExpCRUD.read_areaexp(db, tangara.id_areaexp):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID AreaExp Not Found")
        
        if list(lugares.keys())[0] == "id_areapro" and not AreaProCRUD.read_areapro(db, tangara.id_areapro):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID AreaPro Not Found")
        
        if len(db.query(TangaraModel).filter(TangaraModel.id != id_tangara, TangaraModel.mac == tangara.mac).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Tangara mac must be Unique")
        
        if len(db.query(TangaraModel).filter(TangaraModel.id != id_tangara, TangaraModel.codigo == tangara.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Tangara codigo must be Unique")

        tangara = jsonable_encoder(tangara)
        db.query(TangaraModel).filter(TangaraModel.id == id_tangara).update(tangara)
        db.commit()
        return db.query(TangaraModel).filter(TangaraModel.id == id_tangara).first()

    # Delete

    def delete_tangara(db: Session, id_tangara: int) -> None:
        db.query(TangaraModel).filter(TangaraModel.id == id_tangara).delete()
        db.commit()
