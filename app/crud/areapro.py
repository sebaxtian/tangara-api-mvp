from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.areapro import AreaProModel
from app.schemas.areapro import AreaProSchema, AreaProCreate, AreaProUpdate
from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraSchema


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
        return areapro

    # Read

    def read_areaspro(db: Session, skip: int = 0, limit: int = 100) -> list[AreaProSchema]:
        return db.query(AreaProModel).offset(skip).limit(limit).all()

    def read_areapro(db: Session, id_areapro: int) -> AreaProSchema | None:
        return db.query(AreaProModel).filter(AreaProModel.id == id_areapro).first()
    
    def read_tangaras(db: Session, id_areapro: int, skip: int = 0, limit: int = 100) -> list[TangaraSchema]:
        return db.query(TangaraModel).filter(TangaraModel.id_areapro == id_areapro).offset(skip).limit(limit).all()

    # Update

    def update_areapro(db: Session, id_areapro: int, areapro: AreaProUpdate) -> AreaProSchema | None:
        if len(db.query(AreaProModel).filter(AreaProModel.id != id_areapro, AreaProModel.codigo == areapro.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="AreaPro codigo must be Unique")
        areapro = jsonable_encoder(areapro)
        db.query(AreaProModel).filter(AreaProModel.id == id_areapro).update(areapro)
        db.commit()
        return db.query(AreaProModel).filter(AreaProModel.id == id_areapro).first()

    # Delete

    def delete_areapro(db: Session, id_areapro: int) -> None:
        db.query(AreaProModel).filter(AreaProModel.id == id_areapro).delete()
        db.commit()
