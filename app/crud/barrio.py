from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.comuna import ComunaModel
from app.models.barrio import BarrioModel
from app.schemas.barrio import BarrioSchema, BarrioCreate, BarrioUpdate
from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraSchema


class BarrioCRUD():

    # Create

    def create_barrio(db: Session, barrio: BarrioCreate) -> BarrioSchema:
        barrio = BarrioModel(**barrio.dict())
        if db.query(BarrioModel).filter(BarrioModel.id == barrio.id).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Barrio id must be Unique")
        if not db.query(ComunaModel).filter(ComunaModel.id == barrio.id_comuna).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Comuna Not Found")
        if db.query(BarrioModel).filter(BarrioModel.codigo == barrio.codigo).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Barrio codigo must be Unique")
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
        if len(db.query(BarrioModel).filter(BarrioModel.id != id_barrio, BarrioModel.codigo == barrio.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Barrio codigo must be Unique")
        barrio = jsonable_encoder(barrio)
        db.query(BarrioModel).filter(BarrioModel.id == id_barrio).update(barrio)
        db.commit()
        return db.query(BarrioModel).filter(BarrioModel.id == id_barrio).first()

    # Delete

    def delete_barrio(db: Session, id_barrio: int) -> None:
        db.query(BarrioModel).filter(BarrioModel.id == id_barrio).delete()
        db.commit()