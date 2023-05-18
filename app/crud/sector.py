from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models.vereda import VeredaModel
from models.sector import SectorModel
from schemas.sector import SectorSchema, SectorCreate, SectorUpdate


class SectorCRUD():

    # Create

    def create_sector(db: Session, sector: SectorCreate) -> SectorSchema:
        sector = SectorModel(**sector.dict())
        if not db.query(VeredaModel).filter(VeredaModel.id == sector.id_vereda).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Vereda Not Found")
        db.add(sector)
        db.commit()
        db.refresh(sector)
        return sector

    # Read

    def read_sectores(db: Session, skip: int = 0, limit: int = 100) -> list[SectorSchema]:
        return db.query(SectorModel).offset(skip).limit(limit).all()

    def read_sector(db: Session, id_sector: int) -> SectorSchema | None:
        return db.query(SectorModel).filter(SectorModel.id == id_sector).first()

    # Update

    def update_sector(db: Session, id_sector: int, sector: SectorUpdate) -> SectorSchema | None:
        if not db.query(VeredaModel).filter(VeredaModel.id == sector.id_vereda).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Vereda Not Found")
        sector = jsonable_encoder(sector)
        db.query(SectorModel).filter(SectorModel.id == id_sector).update(sector)
        db.commit()
        return db.query(SectorModel).filter(SectorModel.id == id_sector).first()

    # Delete

    def delete_sector(db: Session, id_sector: int) -> None:
        db.query(SectorModel).filter(SectorModel.id == id_sector).delete()
        db.commit()
