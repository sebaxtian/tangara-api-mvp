from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.comuna import ComunaModel
from app.schemas.comuna import ComunaSchema, ComunaCreate, ComunaUpdate, ComunaPaginationSchema
from app.models.barrio import BarrioModel
from app.schemas.barrio import BarrioPaginationSchema
from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraPaginationSchema


class ComunaCRUD():

    # Create

    def create_comuna(db: Session, comuna: ComunaCreate) -> ComunaSchema:
        comuna = ComunaModel(**comuna.dict())
        if db.query(ComunaModel).filter(ComunaModel.id == comuna.id).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Comuna id must be Unique")
        if db.query(ComunaModel).filter(ComunaModel.codigo == comuna.codigo).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Comuna codigo must be Unique")
        db.add(comuna)
        db.commit()
        db.refresh(comuna)
        return ComunaSchema.validate(comuna)

    # Read

    def read_comunas(db: Session, skip: int = 0, limit: int = None) -> ComunaPaginationSchema:
        comunas = db.query(ComunaModel).offset(skip).limit(limit).all()
        count = len(comunas)
        limit = count if not limit or limit > count else limit
        return ComunaPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "comunas": comunas
        })

    def read_comuna(db: Session, id_comuna: int) -> ComunaSchema:
        comuna = db.query(ComunaModel).filter(ComunaModel.id == id_comuna).first()
        if not comuna:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comuna not found")
        return ComunaSchema.validate(comuna)
    
    def read_barrios(db: Session, id_comuna: int, skip: int = 0, limit: int = None) -> BarrioPaginationSchema:
        barrios = db.query(BarrioModel).filter(BarrioModel.id_comuna == id_comuna).offset(skip).limit(limit).all()
        count = len(barrios)
        limit = count if not limit or limit > count else limit
        return BarrioPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "barrios": barrios
        })
    
    def read_tangaras(db: Session, id_comuna: int, skip: int = 0, limit: int = None) -> TangaraPaginationSchema:
        barrios = db.query(BarrioModel).filter(BarrioModel.id_comuna == id_comuna).all()
        ids_barrios = [barrio.id for barrio in barrios]
        tangaras = db.query(TangaraModel).filter(TangaraModel.id_barrio.in_(ids_barrios)).offset(skip).limit(limit).all()
        count = len(tangaras)
        limit = count if not limit or limit > count else limit
        return TangaraPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "tangaras": tangaras
        })
    

    # Update

    def update_comuna(db: Session, id_comuna: int, comuna: ComunaUpdate) -> ComunaSchema:
        if not db.query(ComunaModel).filter(ComunaModel.id == id_comuna).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comuna not found")
        if len(db.query(ComunaModel).filter(ComunaModel.id != id_comuna, ComunaModel.codigo == comuna.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Comuna codigo must be Unique")
        db.query(ComunaModel).filter(ComunaModel.id == id_comuna).update(jsonable_encoder(comuna))
        db.commit()
        return ComunaSchema.validate(db.query(ComunaModel).filter(ComunaModel.id == id_comuna).first())

    # Delete

    def delete_comuna(db: Session, id_comuna: int) -> None:
        db.query(ComunaModel).filter(ComunaModel.id == id_comuna).delete()
        db.commit()
