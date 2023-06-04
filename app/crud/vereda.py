from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.vereda import VeredaModel
from app.schemas.vereda import VeredaSchema, VeredaCreate, VeredaUpdate
from app.models.sector import SectorModel
from app.schemas.sector import SectorSchema
from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraSchema


class VeredaCRUD():

    # Create

    def create_vereda(db: Session, vereda: VeredaCreate) -> VeredaSchema:
        vereda = VeredaModel(**vereda.dict())
        if db.query(VeredaModel).filter(VeredaModel.id == vereda.id).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Vereda id must be Unique")
        if db.query(VeredaModel).filter(VeredaModel.codigo == vereda.codigo).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Vereda codigo must be Unique")
        db.add(vereda)
        db.commit()
        db.refresh(vereda)
        return vereda

    # Read

    def read_veredas(db: Session, skip: int = 0, limit: int = 100) -> list[VeredaSchema]:
        return db.query(VeredaModel).offset(skip).limit(limit).all()

    def read_vereda(db: Session, id_vereda: int) -> VeredaSchema | None:
        return db.query(VeredaModel).filter(VeredaModel.id == id_vereda).first()
    
    def read_sectores(db: Session, id_vereda: int, skip: int = 0, limit: int = 100) -> list[SectorSchema]:
        return db.query(SectorModel).filter(SectorModel.id_vereda == id_vereda).offset(skip).limit(limit).all()
    
    def read_tangaras(db: Session, id_vereda: int, skip: int = 0, limit: int = 100) -> list[TangaraSchema]:
        sectores = db.query(SectorModel).filter(SectorModel.id_vereda == id_vereda).all()
        ids_sectores = [sector.id for sector in sectores]
        return db.query(TangaraModel).filter(TangaraModel.id_sector.in_(ids_sectores)).offset(skip).limit(limit).all()

    # Update

    def update_vereda(db: Session, id_vereda: int, vereda: VeredaUpdate) -> VeredaSchema | None:
        if len(db.query(VeredaModel).filter(VeredaModel.id != id_vereda, VeredaModel.codigo == vereda.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Vereda codigo must be Unique")
        vereda = jsonable_encoder(vereda)
        db.query(VeredaModel).filter(VeredaModel.id == id_vereda).update(vereda)
        db.commit()
        return db.query(VeredaModel).filter(VeredaModel.id == id_vereda).first()

    # Delete

    def delete_vereda(db: Session, id_vereda: int) -> None:
        db.query(VeredaModel).filter(VeredaModel.id == id_vereda).delete()
        db.commit()
