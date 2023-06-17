from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraSchema, TangaraCreate, TangaraUpdate, TangaraPaginationSchema
from app.crud.barrio import BarrioCRUD
from app.crud.sector import SectorCRUD
from app.crud.areaexp import AreaExpCRUD
from app.crud.areapro import AreaProCRUD


class TangaraCRUD():

    # Create

    def create_tangara(db: Session, tangara: TangaraCreate) -> TangaraSchema:
        lugares = jsonable_encoder({
            "id_barrio": tangara.id_barrio,
            "id_sector": tangara.id_sector,
            "id_areaexp": tangara.id_areaexp,
            "id_areapro": tangara.id_areapro
        }, exclude_none=True)

        if db.query(TangaraModel).filter(TangaraModel.id == tangara.id).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Tangara id must be Unique")

        if len(list(lugares.keys())) > 1:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only one accepted: id_barrio, id_sector, id_areaexp, id_areapro")

        if not lugares.keys():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Any of id_barrio, id_sector, id_areaexp, id_areapro is required")

        if list(lugares.keys())[0] == "id_barrio" and not BarrioCRUD.read_barrio(db, tangara.id_barrio):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Barrio not found")
        
        if list(lugares.keys())[0] == "id_sector" and not SectorCRUD.read_sector(db, tangara.id_sector):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sector not found")
        
        if list(lugares.keys())[0] == "id_areaexp" and not AreaExpCRUD.read_areaexp(db, tangara.id_areaexp):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AreaExp not found")
        
        if list(lugares.keys())[0] == "id_areapro" and not AreaProCRUD.read_areapro(db, tangara.id_areapro):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AreaPro not found")
        
        if db.query(TangaraModel).filter(TangaraModel.mac == tangara.mac).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Tangara mac must be Unique")
        
        if db.query(TangaraModel).filter(TangaraModel.codigo == tangara.codigo).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Tangara codigo must be Unique")
        
        tangara = TangaraModel(**tangara.dict())
        db.add(tangara)
        db.commit()
        db.refresh(tangara)
        return TangaraSchema.validate(tangara)

    # Read

    def read_tangaras(db: Session, skip: int = 0, limit: int = None) -> TangaraPaginationSchema:
        tangaras = db.query(TangaraModel).offset(skip).limit(limit).all()
        count = len(tangaras)
        limit = count if not limit or limit > count else limit
        return TangaraPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "tangaras": tangaras
        })
    
    def read_tangara(db: Session, id_tangara: int) -> TangaraSchema:
        tangara = db.query(TangaraModel).filter(TangaraModel.id == id_tangara).first()
        if not tangara:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tangara not found")
        return TangaraSchema.validate(tangara)

    # Update

    def update_tangara(db: Session, id_tangara: int, tangara: TangaraUpdate) -> TangaraSchema:
        lugares = jsonable_encoder({
            "id_barrio": tangara.id_barrio,
            "id_sector": tangara.id_sector,
            "id_areaexp": tangara.id_areaexp,
            "id_areapro": tangara.id_areapro
        }, exclude_none=True)

        if len(list(lugares.keys())) > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only one accepted: id_barrio, id_sector, id_areaexp, id_areapro")

        if list(lugares.keys())[0] == "id_barrio" and not BarrioCRUD.read_barrio(db, tangara.id_barrio):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Barrio not found")
        
        if list(lugares.keys())[0] == "id_sector" and not SectorCRUD.read_sector(db, tangara.id_sector):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sector not found")
        
        if list(lugares.keys())[0] == "id_areaexp" and not AreaExpCRUD.read_areaexp(db, tangara.id_areaexp):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AreaExp not found")
        
        if list(lugares.keys())[0] == "id_areapro" and not AreaProCRUD.read_areapro(db, tangara.id_areapro):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AreaPro not found")
        
        if len(db.query(TangaraModel).filter(TangaraModel.id != id_tangara, TangaraModel.mac == tangara.mac).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Tangara mac must be Unique")
        
        if len(db.query(TangaraModel).filter(TangaraModel.id != id_tangara, TangaraModel.codigo == tangara.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Tangara codigo must be Unique")

        tangara = jsonable_encoder(tangara)
        db.query(TangaraModel).filter(TangaraModel.id == id_tangara).update(tangara)
        db.commit()
        return TangaraSchema.validate(db.query(TangaraModel).filter(TangaraModel.id == id_tangara).first())

    # Delete

    def delete_tangara(db: Session, id_tangara: int) -> None:
        db.query(TangaraModel).filter(TangaraModel.id == id_tangara).delete()
        db.commit()
