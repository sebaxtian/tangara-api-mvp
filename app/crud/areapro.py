from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.areapro import AreaProModel
from app.schemas.areapro import AreaProSchema, AreaProCreate, AreaProUpdate, AreaProPaginationSchema
from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraPaginationSchema


class AreaProCRUD():

    # Create

    def create_areapro(db: Session, areapro: AreaProCreate) -> AreaProSchema:
        areapro = AreaProModel(**areapro.dict())
        if db.query(AreaProModel).filter(AreaProModel.id == areapro.id).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="AreaPro id must be Unique")
        if db.query(AreaProModel).filter(AreaProModel.codigo == areapro.codigo).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="AreaPro codigo must be Unique")
        db.add(areapro)
        db.commit()
        db.refresh(areapro)
        return AreaProSchema.validate(areapro)

    # Read

    def read_areaspro(db: Session, skip: int = 0, limit: int = None) -> AreaProPaginationSchema:
        areaspro = db.query(AreaProModel).offset(skip).limit(limit).all()
        count = len(areaspro)
        limit = count if not limit or limit > count else limit
        return AreaProPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "areaspro": areaspro
        })

    def read_areapro(db: Session, id_areapro: int) -> AreaProSchema:
        areapro = db.query(AreaProModel).filter(AreaProModel.id == id_areapro).first()
        if not areapro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AreaPro not found")
        return AreaProSchema.validate(areapro)
    
    def read_tangaras(db: Session, id_areapro: int, skip: int = 0, limit: int = None) -> TangaraPaginationSchema:
        tangaras = db.query(TangaraModel).filter(TangaraModel.id_areapro == id_areapro).offset(skip).limit(limit).all()
        count = len(tangaras)
        limit = count if not limit or limit > count else limit
        return TangaraPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "tangaras": tangaras
        })

    # Update

    def update_areapro(db: Session, id_areapro: int, areapro: AreaProUpdate) -> AreaProSchema:
        if len(db.query(AreaProModel).filter(AreaProModel.id != id_areapro, AreaProModel.codigo == areapro.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="AreaPro codigo must be Unique")
        areapro = jsonable_encoder(areapro)
        db.query(AreaProModel).filter(AreaProModel.id == id_areapro).update(areapro)
        db.commit()
        return AreaProSchema.validate(db.query(AreaProModel).filter(AreaProModel.id == id_areapro).first())

    # Delete

    def delete_areapro(db: Session, id_areapro: int) -> None:
        db.query(AreaProModel).filter(AreaProModel.id == id_areapro).delete()
        db.commit()
