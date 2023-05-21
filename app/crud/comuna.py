from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.comuna import ComunaModel
from schemas.comuna import ComunaSchema, ComunaCreate, ComunaUpdate
from models.barrio import BarrioModel
from schemas.barrio import BarrioSchema
from models.tangara import TangaraModel
from schemas.tangara import TangaraSchema


class ComunaCRUD():

    # Create

    def create_comuna(db: Session, comuna: ComunaCreate) -> ComunaSchema:
        comuna = ComunaModel(**comuna.dict())
        if db.query(ComunaModel).filter(ComunaModel.codigo == comuna.codigo).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Comuna codigo must be Unique")
        db.add(comuna)
        db.commit()
        db.refresh(comuna)
        return comuna

    # Read

    def read_comunas(db: Session, skip: int = 0, limit: int = 100) -> list[ComunaSchema]:
        return db.query(ComunaModel).offset(skip).limit(limit).all()

    def read_comuna(db: Session, id_comuna: int) -> ComunaSchema | None:
        return db.query(ComunaModel).filter(ComunaModel.id == id_comuna).first()
    
    def read_barrios(db: Session, id_comuna: int, skip: int = 0, limit: int = 100) -> list[BarrioSchema]:
        return db.query(BarrioModel).filter(BarrioModel.id_comuna == id_comuna).offset(skip).limit(limit).all()
    
    def read_tangaras(db: Session, id_comuna: int, skip: int = 0, limit: int = 100) -> list[TangaraSchema]:
        barrios = db.query(BarrioModel).filter(BarrioModel.id_comuna == id_comuna).all()
        ids_barrios = [barrio.id for barrio in barrios]
        return db.query(TangaraModel).filter(TangaraModel.id_barrio.in_(ids_barrios)).offset(skip).limit(limit).all()

    # Update

    def update_comuna(db: Session, id_comuna: int, comuna: ComunaUpdate) -> ComunaSchema | None:
        if len(db.query(ComunaModel).filter(ComunaModel.id != id_comuna, ComunaModel.codigo == comuna.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Comuna codigo must be Unique")
        comuna = jsonable_encoder(comuna)
        db.query(ComunaModel).filter(ComunaModel.id == id_comuna).update(comuna)
        db.commit()
        return db.query(ComunaModel).filter(ComunaModel.id == id_comuna).first()

    # Delete

    def delete_comuna(db: Session, id_comuna: int) -> None:
        db.query(ComunaModel).filter(ComunaModel.id == id_comuna).delete()
        db.commit()
