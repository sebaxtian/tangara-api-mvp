from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.vereda import VeredaModel
from schemas.vereda import VeredaSchema, VeredaCreate, VeredaUpdate


class VeredaCRUD():

    # Create

    def create_vereda(db: Session, vereda: VeredaCreate) -> VeredaSchema:
        vereda = VeredaModel(**vereda.dict())
        db.add(vereda)
        db.commit()
        db.refresh(vereda)
        return vereda

    # Read

    def read_veredas(db: Session, skip: int = 0, limit: int = 100) -> list[VeredaSchema]:
        return db.query(VeredaModel).offset(skip).limit(limit).all()

    def read_vereda(db: Session, id_vereda: int) -> VeredaSchema | None:
        return db.query(VeredaModel).filter(VeredaModel.id == id_vereda).first()

    # Update

    def update_vereda(db: Session, id_vereda: int, vereda: VeredaUpdate) -> VeredaSchema | None:
        vereda = jsonable_encoder(vereda)
        db.query(VeredaModel).filter(VeredaModel.id == id_vereda).update(vereda)
        db.commit()
        return db.query(VeredaModel).filter(VeredaModel.id == id_vereda).first()

    # Delete

    def delete_vereda(db: Session, id_vereda: int) -> None:
        db.query(VeredaModel).filter(VeredaModel.id == id_vereda).delete()
        db.commit()
