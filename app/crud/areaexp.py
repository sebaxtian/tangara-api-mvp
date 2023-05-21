from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.areaexp import AreaExpModel
from schemas.areaexp import AreaExpSchema, AreaExpCreate, AreaExpUpdate
from models.tangara import TangaraModel
from schemas.tangara import TangaraSchema


class AreaExpCRUD():

    # Create

    def create_areaexp(db: Session, areaexp: AreaExpCreate) -> AreaExpSchema:
        areaexp = AreaExpModel(**areaexp.dict())
        db.add(areaexp)
        db.commit()
        db.refresh(areaexp)
        return areaexp

    # Read

    def read_areasexp(db: Session, skip: int = 0, limit: int = 100) -> list[AreaExpSchema]:
        return db.query(AreaExpModel).offset(skip).limit(limit).all()

    def read_areaexp(db: Session, id_areaexp: int) -> AreaExpSchema | None:
        return db.query(AreaExpModel).filter(AreaExpModel.id == id_areaexp).first()
    
    def read_tangaras(db: Session, id_areaexp: int, skip: int = 0, limit: int = 100) -> list[TangaraSchema]:
        return db.query(TangaraModel).filter(TangaraModel.id_areaexp == id_areaexp).offset(skip).limit(limit).all()

    # Update

    def update_areaexp(db: Session, id_areaexp: int, areaexp: AreaExpUpdate) -> AreaExpSchema | None:
        areaexp = jsonable_encoder(areaexp)
        db.query(AreaExpModel).filter(AreaExpModel.id == id_areaexp).update(areaexp)
        db.commit()
        return db.query(AreaExpModel).filter(AreaExpModel.id == id_areaexp).first()

    # Delete

    def delete_areaexp(db: Session, id_areaexp: int) -> None:
        db.query(AreaExpModel).filter(AreaExpModel.id == id_areaexp).delete()
        db.commit()
