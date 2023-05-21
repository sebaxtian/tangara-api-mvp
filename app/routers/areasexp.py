from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from dependencies.db import get_db
from schemas.areaexp import AreaExpSchema, AreaExpCreate, AreaExpUpdate
from crud.areaexp import AreaExpCRUD
from schemas.tangara import TangaraSchema


router = APIRouter(
    prefix="/areasexp",
    tags=["areasexp"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=list[AreaExpSchema], status_code=status.HTTP_200_OK)
async def areasexp(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[AreaExpSchema]:
    areasexp = AreaExpCRUD.read_areasexp(db, skip=skip, limit=limit)
    return areasexp


@router.get("/{id}", response_model=AreaExpSchema, status_code=status.HTTP_200_OK)
async def areasexp(id: int, db: Session = Depends(get_db)) -> AreaExpSchema:
    areaexp = AreaExpCRUD.read_areaexp(db, id_areaexp=id)
    if not areaexp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return areaexp


@router.post("/", response_model=AreaExpSchema, status_code=status.HTTP_201_CREATED)
async def areasexp(areaexp: AreaExpCreate, db: Session = Depends(get_db)) -> AreaExpSchema:
    areaexp = AreaExpCRUD.create_areaexp(db, areaexp=areaexp)
    return areaexp


@router.put("/{id}", response_model=AreaExpSchema, status_code=status.HTTP_200_OK)
async def areasexp(id: int, areaexp: AreaExpUpdate, db: Session = Depends(get_db)) -> AreaExpSchema:
    areaexp = AreaExpCRUD.update_areaexp(db, id_areaexp=id, areaexp=areaexp)
    if not areaexp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return areaexp


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def areasexp(id: int, db: Session = Depends(get_db)) -> None:
    AreaExpCRUD.delete_areaexp(db, id_areaexp=id)


@router.get("/{id}/tangaras", response_model=list[TangaraSchema], status_code=status.HTTP_200_OK)
async def areasexp(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[TangaraSchema]:
    tangaras = AreaExpCRUD.read_tangaras(db, id_areaexp=id, skip=skip, limit=limit)
    return tangaras
