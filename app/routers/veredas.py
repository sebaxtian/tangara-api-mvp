from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from datetime import timedelta

from app.dependencies.database import get_db
from app.schemas.vereda import VeredaSchema, VeredaCreate, VeredaUpdate, VeredaPaginationSchema
from app.crud.vereda import VeredaCRUD
from app.schemas.sector import SectorPaginationSchema
from app.schemas.tangara import TangaraPaginationSchema


router = APIRouter(
    prefix="/veredas",
    tags=["veredas"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=VeredaPaginationSchema, status_code=status.HTTP_200_OK)
@cache(namespace="veredas", expire=timedelta(days=30))
async def veredas(skip: int = 0, limit: int = None, db: Session = Depends(get_db)) -> VeredaPaginationSchema:
    veredas = VeredaCRUD.read_veredas(db, skip=skip, limit=limit)
    return veredas


@router.get("/{id}", response_model=VeredaSchema, status_code=status.HTTP_200_OK)
@cache(namespace="veredas", expire=timedelta(days=30))
async def veredas(id: int, db: Session = Depends(get_db)) -> VeredaSchema:
    vereda = VeredaCRUD.read_vereda(db, id_vereda=id)
    if not vereda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return vereda


@router.post("/", response_model=VeredaSchema, status_code=status.HTTP_201_CREATED)
async def veredas(vereda: VeredaCreate, db: Session = Depends(get_db)) -> VeredaSchema:
    vereda = VeredaCRUD.create_vereda(db, vereda=vereda)
    await FastAPICache.clear(namespace="veredas")
    return vereda


@router.put("/{id}", response_model=VeredaSchema, status_code=status.HTTP_200_OK)
async def veredas(id: int, vereda: VeredaUpdate, db: Session = Depends(get_db)) -> VeredaSchema:
    vereda = VeredaCRUD.update_vereda(db, id_vereda=id, vereda=vereda)
    if not vereda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await FastAPICache.clear(namespace="veredas")
    return vereda


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def veredas(id: int, db: Session = Depends(get_db)) -> None:
    VeredaCRUD.delete_vereda(db, id_vereda=id)
    await FastAPICache.clear(namespace="veredas")


@router.get("/{id}/sectores", response_model=SectorPaginationSchema, status_code=status.HTTP_200_OK)
@cache(namespace="veredas", expire=timedelta(days=30))
async def veredas(id: int, skip: int = 0, limit: int = None, db: Session = Depends(get_db)) -> SectorPaginationSchema:
    sectores = VeredaCRUD.read_sectores(db, id_vereda=id, skip=skip, limit=limit)
    return sectores


@router.get("/{id}/tangaras", response_model=TangaraPaginationSchema, status_code=status.HTTP_200_OK)
@cache(namespace="veredas", expire=timedelta(days=30))
async def veredas(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> TangaraPaginationSchema:
    tangaras = VeredaCRUD.read_tangaras(db, id_vereda=id, skip=skip, limit=limit)
    return tangaras
