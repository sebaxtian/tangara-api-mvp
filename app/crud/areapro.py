from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.areapro import AreaProModel
from schemas.areapro import AreaProSchema, AreaProCreate, AreaProUpdate


class AreaProCRUD():

    # Create

    def create_areapro(db: Session, areapro: AreaProCreate) -> AreaProSchema:
        areapro = AreaProModel(**areapro.dict())
        db.add(areapro)
        db.commit()
        db.refresh(areapro)
        return areapro

    # Read

    def read_areaspro(db: Session, skip: int = 0, limit: int = 100) -> list[AreaProSchema]:
        return db.query(AreaProModel).offset(skip).limit(limit).all()

    def read_areapro(db: Session, id_areapro: int) -> AreaProSchema | None:
        return db.query(AreaProModel).filter(AreaProModel.id == id_areapro).first()

    # Update

    def update_areapro(db: Session, id_areapro: int, areapro: AreaProUpdate) -> AreaProSchema | None:
        areapro = jsonable_encoder(areapro)
        db.query(AreaProModel).filter(AreaProModel.id == id_areapro).update(areapro)
        db.commit()
        return db.query(AreaProModel).filter(AreaProModel.id == id_areapro).first()

    # Delete

    def delete_areapro(db: Session, id_areapro: int) -> None:
        db.query(AreaProModel).filter(AreaProModel.id == id_areapro).delete()
        db.commit()
