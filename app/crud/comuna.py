from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.comuna import ComunaModel
from schemas.comuna import ComunaSchema, ComunaCreate, ComunaUpdate


class ComunaCRUD():

    # Create

    def create_comuna(db: Session, comuna: ComunaCreate) -> ComunaSchema:
        comuna = ComunaModel(**comuna.dict())
        db.add(comuna)
        db.commit()
        db.refresh(comuna)
        return comuna

    # Read

    def read_comunas(db: Session, skip: int = 0, limit: int = 100) -> list[ComunaSchema]:
        return db.query(ComunaModel).offset(skip).limit(limit).all()

    def read_comuna(db: Session, id_comuna: int) -> ComunaSchema | None:
        return db.query(ComunaModel).filter(ComunaModel.id == id_comuna).first()

    # Update

    def update_comuna(db: Session, id_comuna: int, comuna: ComunaUpdate) -> ComunaSchema | None:
        comuna = jsonable_encoder(comuna)
        db.query(ComunaModel).filter(ComunaModel.id == id_comuna).update(comuna)
        db.commit()
        return db.query(ComunaModel).filter(ComunaModel.id == id_comuna).first()

    # Delete

    def delete_comuna(db: Session, id_comuna: int) -> None:
        db.query(ComunaModel).filter(ComunaModel.id == id_comuna).delete()
        db.commit()
