from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.vereda import VeredaModel
from app.models.sector import SectorModel
from app.schemas.sector import SectorSchema, SectorCreate, SectorUpdate, SectorPaginationSchema
from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraPaginationSchema


class SectorCRUD():

    # Create

    def create_sector(db: Session, sector: SectorCreate) -> SectorSchema:
        sector = SectorModel(**sector.dict())
        if db.query(SectorModel).filter(SectorModel.id == sector.id).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Sector id must be Unique")
        if not db.query(VeredaModel).filter(VeredaModel.id == sector.id_vereda).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Vereda Not Found")
        if db.query(SectorModel).filter(SectorModel.codigo == sector.codigo).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Sector codigo must be Unique")
        db.add(sector)
        db.commit()
        db.refresh(sector)
        return SectorSchema.validate(sector)

    # Read

    def read_sectores(db: Session, skip: int = 0, limit: int = None) -> SectorPaginationSchema:
        sectores = db.query(SectorModel).offset(skip).limit(limit).all()
        count = len(sectores)
        limit = count if not limit or limit > count else limit
        return SectorPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "sectores": sectores
        })

    def read_sector(db: Session, id_sector: int) -> SectorSchema:
        sector = db.query(SectorModel).filter(SectorModel.id == id_sector).first()
        if not sector:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sector not found")
        return SectorSchema.validate(sector)
    
    def read_tangaras(db: Session, id_sector: int, skip: int = 0, limit: int = None) -> TangaraPaginationSchema:
        tangaras = db.query(TangaraModel).filter(TangaraModel.id_sector == id_sector).offset(skip).limit(limit).all()
        count = len(tangaras)
        limit = count if not limit or limit > count else limit
        return TangaraPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "tangaras": tangaras
        })

    # Update

    def update_sector(db: Session, id_sector: int, sector: SectorUpdate) -> SectorSchema:
        if not db.query(VeredaModel).filter(VeredaModel.id == sector.id_vereda).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Vereda Not Found")
        if len(db.query(SectorModel).filter(SectorModel.id != id_sector, SectorModel.codigo == sector.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Sector codigo must be Unique")
        db.query(SectorModel).filter(SectorModel.id == id_sector).update(jsonable_encoder(sector))
        db.commit()
        return SectorSchema.validate(db.query(SectorModel).filter(SectorModel.id == id_sector).first())

    # Delete

    def delete_sector(db: Session, id_sector: int) -> None:
        db.query(SectorModel).filter(SectorModel.id == id_sector).delete()
        db.commit()
