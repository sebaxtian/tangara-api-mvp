from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.comuna import ComunaModel
from models.barrio import BarrioModel
from schemas.barrio import BarrioSchema, BarrioCreate, BarrioUpdate
from models.tangara import TangaraModel
from schemas.tangara import TangaraSchema


class BarrioCRUD():

    # Create

    def create_barrio(db: Session, barrio: BarrioCreate) -> BarrioSchema:
        barrio = BarrioModel(**barrio.dict())
        if not db.query(ComunaModel).filter(ComunaModel.id == barrio.id_comuna).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Comuna Not Found")
        db.add(barrio)
        db.commit()
        db.refresh(barrio)
        return barrio

    # Read

    def read_barrios(db: Session, skip: int = 0, limit: int = 100) -> list[BarrioSchema]:
        return db.query(BarrioModel).offset(skip).limit(limit).all()

    def read_barrio(db: Session, id_barrio: int) -> BarrioSchema | None:
        return db.query(BarrioModel).filter(BarrioModel.id == id_barrio).first()
    
    def read_tangaras(db: Session, id_barrio: int, skip: int = 0, limit: int = 100) -> list[TangaraSchema]:
        return db.query(TangaraModel).filter(TangaraModel.id_barrio == id_barrio).offset(skip).limit(limit).all()

    # Update

    def update_barrio(db: Session, id_barrio: int, barrio: BarrioUpdate) -> BarrioSchema | None:
        if not db.query(ComunaModel).filter(ComunaModel.id == barrio.id_comuna).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Comuna Not Found")
        barrio = jsonable_encoder(barrio)
        db.query(BarrioModel).filter(BarrioModel.id == id_barrio).update(barrio)
        db.commit()
        return db.query(BarrioModel).filter(BarrioModel.id == id_barrio).first()

    # Delete

    def delete_barrio(db: Session, id_barrio: int) -> None:
        db.query(BarrioModel).filter(BarrioModel.id == id_barrio).delete()
        db.commit()
