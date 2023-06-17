from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.areaexp import AreaExpModel
from app.schemas.areaexp import AreaExpSchema, AreaExpCreate, AreaExpUpdate, AreaExpPaginationSchema
from app.models.tangara import TangaraModel
from app.schemas.tangara import TangaraPaginationSchema


class AreaExpCRUD():

    # Create

    def create_areaexp(db: Session, areaexp: AreaExpCreate) -> AreaExpSchema:
        areaexp = AreaExpModel(**areaexp.dict())
        if db.query(AreaExpModel).filter(AreaExpModel.id == areaexp.id).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="AreaExp id must be Unique")
        if db.query(AreaExpModel).filter(AreaExpModel.codigo == areaexp.codigo).first():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="AreaExp codigo must be Unique")
        db.add(areaexp)
        db.commit()
        db.refresh(areaexp)
        return AreaExpSchema.validate(areaexp)

    # Read

    def read_areasexp(db: Session, skip: int = 0, limit: int = None) -> AreaExpPaginationSchema:
        areasexp = db.query(AreaExpModel).offset(skip).limit(limit).all()
        count = len(areasexp)
        limit = count if not limit or limit > count else limit
        return AreaExpPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "areasexp": areasexp
        })

    def read_areaexp(db: Session, id_areaexp: int) -> AreaExpSchema:
        areaexp = db.query(AreaExpModel).filter(AreaExpModel.id == id_areaexp).first()
        if not areaexp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AreaExp not found")
        return AreaExpSchema.validate(areaexp)
    
    def read_tangaras(db: Session, id_areaexp: int, skip: int = 0, limit: int = None) -> TangaraPaginationSchema:
        tangaras = db.query(TangaraModel).filter(TangaraModel.id_areaexp == id_areaexp).offset(skip).limit(limit).all()
        count = len(tangaras)
        limit = count if not limit or limit > count else limit
        return TangaraPaginationSchema.validate({
            "count": count, 
            "skip": skip, 
            "limit": limit, 
            "tangaras": tangaras
        })

    # Update

    def update_areaexp(db: Session, id_areaexp: int, areaexp: AreaExpUpdate) -> AreaExpSchema:
        if len(db.query(AreaExpModel).filter(AreaExpModel.id != id_areaexp, AreaExpModel.codigo == areaexp.codigo).all()) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="AreaExp codigo must be Unique")
        areaexp = jsonable_encoder(areaexp)
        db.query(AreaExpModel).filter(AreaExpModel.id == id_areaexp).update(areaexp)
        db.commit()
        return AreaExpSchema.validate(db.query(AreaExpModel).filter(AreaExpModel.id == id_areaexp).first())

    # Delete

    def delete_areaexp(db: Session, id_areaexp: int) -> None:
        db.query(AreaExpModel).filter(AreaExpModel.id == id_areaexp).delete()
        db.commit()
