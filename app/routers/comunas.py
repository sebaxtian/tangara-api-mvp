from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from datetime import timedelta

from app.dependencies.database import get_db
from app.schemas.comuna import ComunaSchema, ComunaCreate, ComunaUpdate, ComunaPaginationSchema
from app.crud.comuna import ComunaCRUD
from app.schemas.barrio import BarrioPaginationSchema
from app.schemas.tangara import TangaraPaginationSchema


router = APIRouter(
    prefix="/comunas",
    tags=["comunas"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=ComunaPaginationSchema, status_code=status.HTTP_200_OK)
@cache(namespace="comunas", expire=timedelta(days=30))
async def comunas(skip: int = 0, limit: int = None, db: Session = Depends(get_db)) -> ComunaPaginationSchema:
    comunas = ComunaCRUD.read_comunas(db, skip=skip, limit=limit)
    return comunas


@router.get("/{id}", response_model=ComunaSchema, status_code=status.HTTP_200_OK)
@cache(namespace="comunas", expire=timedelta(days=30))
async def comunas(id: int, db: Session = Depends(get_db)) -> ComunaSchema:
    comuna = ComunaCRUD.read_comuna(db, id_comuna=id)
    if not comuna:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return comuna


@router.post("/", response_model=ComunaSchema, status_code=status.HTTP_201_CREATED)
async def comunas(comuna: ComunaCreate, db: Session = Depends(get_db)) -> ComunaSchema:
    comuna = ComunaCRUD.create_comuna(db, comuna=comuna)
    #await FastAPICache.clear(namespace="comunas")
    return comuna


@router.put("/{id}", response_model=ComunaSchema, status_code=status.HTTP_200_OK)
async def comunas(id: int, comuna: ComunaUpdate, db: Session = Depends(get_db)) -> ComunaSchema:
    comuna = ComunaCRUD.update_comuna(db, id_comuna=id, comuna=comuna)
    if not comuna:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #await FastAPICache.clear(namespace="comunas")
    return comuna


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def comunas(id: int, db: Session = Depends(get_db)) -> None:
    ComunaCRUD.delete_comuna(db, id_comuna=id)
    #await FastAPICache.clear(namespace="comunas")


@router.get("/{id}/barrios", response_model=BarrioPaginationSchema, status_code=status.HTTP_200_OK)
@cache(namespace="comunas", expire=timedelta(days=30))
async def comunas(id: int, skip: int = 0, limit: int = None, db: Session = Depends(get_db)) -> BarrioPaginationSchema:
    barrios = ComunaCRUD.read_barrios(db, id_comuna=id, skip=skip, limit=limit)
    return barrios


@router.get("/{id}/tangaras", response_model=TangaraPaginationSchema, status_code=status.HTTP_200_OK)
@cache(namespace="comunas", expire=timedelta(days=30))
async def comunas(id: int, skip: int = 0, limit: int = None, db: Session = Depends(get_db)) -> TangaraPaginationSchema:
    tangaras = ComunaCRUD.read_tangaras(db, id_comuna=id, skip=skip, limit=limit)
    return tangaras
