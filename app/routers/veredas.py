from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from dependencies.db import get_db
from schemas.vereda import VeredaSchema, VeredaCreate, VeredaUpdate
from crud.vereda import VeredaCRUD
from schemas.sector import SectorSchema
from schemas.tangara import TangaraSchema


router = APIRouter(
    prefix="/veredas",
    tags=["veredas"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=list[VeredaSchema], status_code=status.HTTP_200_OK)
async def veredas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[VeredaSchema]:
    veredas = VeredaCRUD.read_veredas(db, skip=skip, limit=limit)
    return veredas


@router.get("/{id}", response_model=VeredaSchema, status_code=status.HTTP_200_OK)
async def veredas(id: int, db: Session = Depends(get_db)) -> VeredaSchema:
    vereda = VeredaCRUD.read_vereda(db, id_vereda=id)
    if not vereda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return vereda


@router.post("/", response_model=VeredaSchema, status_code=status.HTTP_201_CREATED)
async def veredas(vereda: VeredaCreate, db: Session = Depends(get_db)) -> VeredaSchema:
    vereda = VeredaCRUD.create_vereda(db, vereda=vereda)
    return vereda


@router.put("/{id}", response_model=VeredaSchema, status_code=status.HTTP_200_OK)
async def veredas(id: int, vereda: VeredaUpdate, db: Session = Depends(get_db)) -> VeredaSchema:
    vereda = VeredaCRUD.update_vereda(db, id_vereda=id, vereda=vereda)
    if not vereda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return vereda


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def veredas(id: int, db: Session = Depends(get_db)) -> None:
    VeredaCRUD.delete_vereda(db, id_vereda=id)


@router.get("/{id}/sectores", response_model=list[SectorSchema], status_code=status.HTTP_200_OK)
async def veredas(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[SectorSchema]:
    sectores = VeredaCRUD.read_sectores(db, id_vereda=id, skip=skip, limit=limit)
    return sectores


@router.get("/{id}/tangaras", response_model=list[TangaraSchema], status_code=status.HTTP_200_OK)
async def veredas(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[TangaraSchema]:
    tangaras = VeredaCRUD.read_tangaras(db, id_vereda=id, skip=skip, limit=limit)
    return tangaras
