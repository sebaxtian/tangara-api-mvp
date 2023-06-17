from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.vereda import VeredaModel
from app.schemas.vereda import VeredaSchema, VeredaCreate, VeredaUpdate, VeredaPaginationSchema
from app.models.sector import SectorModel
from app.schemas.sector import SectorPaginationSchema
from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraPaginationSchema


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
        return VeredaSchema.validate(vereda)

    # Read

    def read_veredas(db: Session, skip: int = 0, limit: int = None) -> VeredaPaginationSchema:
        veredas = db.query(VeredaModel).offset(skip).limit(limit).all()
        count = len(veredas)
        limit = count if not limit or limit > count else limit
        return VeredaPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "veredas": veredas
        })

    def read_vereda(db: Session, id_vereda: int) -> VeredaSchema:
        vereda = db.query(VeredaModel).filter(VeredaModel.id == id_vereda).first()
        if not vereda:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vereda not found")
        return VeredaSchema.validate(vereda)
    
    def read_sectores(db: Session, id_vereda: int, skip: int = 0, limit: int = None) -> SectorPaginationSchema:
        sectores = db.query(SectorModel).filter(SectorModel.id_vereda == id_vereda).offset(skip).limit(limit).all()
        count = len(sectores)
        limit = count if not limit or limit > count else limit
        return SectorPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "sectores": sectores
        })
    
    def read_tangaras(db: Session, id_vereda: int, skip: int = 0, limit: int = None) -> TangaraPaginationSchema:
        sectores = db.query(SectorModel).filter(SectorModel.id_vereda == id_vereda).all()
        ids_sectores = [sector.id for sector in sectores]
        tangaras = db.query(TangaraModel).filter(TangaraModel.id_sector.in_(ids_sectores)).offset(skip).limit(limit).all()
        count = len(tangaras)
        limit = count if not limit or limit > count else limit
        return TangaraPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "tangaras": tangaras
        })

    # Update

    def update_vereda(db: Session, id_vereda: int, vereda: VeredaUpdate) -> VeredaSchema:
        vereda = db.query(VeredaModel).filter(VeredaModel.id == id_vereda).first()
        if not vereda:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vereda not found")
        if len(db.query(VeredaModel).filter(VeredaModel.id != id_vereda, VeredaModel.codigo == vereda.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Vereda codigo must be Unique")
        vereda = jsonable_encoder(vereda)
        db.query(VeredaModel).filter(VeredaModel.id == id_vereda).update(vereda)
        db.commit()
        return VeredaSchema.validate(db.query(VeredaModel).filter(VeredaModel.id == id_vereda).first())

    # Delete

    def delete_vereda(db: Session, id_vereda: int) -> None:
        db.query(VeredaModel).filter(VeredaModel.id == id_vereda).delete()
        db.commit()
