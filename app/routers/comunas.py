from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.comuna import ComunaSchema, ComunaCreate, ComunaUpdate
from app.crud.comuna import ComunaCRUD
from app.schemas.barrio import BarrioSchema
from app.schemas.tangara import TangaraSchema


router = APIRouter(
    prefix="/comunas",
    tags=["comunas"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=list[ComunaSchema], status_code=status.HTTP_200_OK)
async def comunas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[ComunaSchema]:
    comunas = ComunaCRUD.read_comunas(db, skip=skip, limit=limit)
    return comunas


@router.get("/{id}", response_model=ComunaSchema, status_code=status.HTTP_200_OK)
async def comunas(id: int, db: Session = Depends(get_db)) -> ComunaSchema:
    comuna = ComunaCRUD.read_comuna(db, id_comuna=id)
    if not comuna:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return comuna


@router.post("/", response_model=ComunaSchema, status_code=status.HTTP_201_CREATED)
async def comunas(comuna: ComunaCreate, db: Session = Depends(get_db)) -> ComunaSchema:
    comuna = ComunaCRUD.create_comuna(db, comuna=comuna)
    return comuna


@router.put("/{id}", response_model=ComunaSchema, status_code=status.HTTP_200_OK)
async def comunas(id: int, comuna: ComunaUpdate, db: Session = Depends(get_db)) -> ComunaSchema:
    comuna = ComunaCRUD.update_comuna(db, id_comuna=id, comuna=comuna)
    if not comuna:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return comuna


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def comunas(id: int, db: Session = Depends(get_db)) -> None:
    ComunaCRUD.delete_comuna(db, id_comuna=id)


@router.get("/{id}/barrios", response_model=list[BarrioSchema], status_code=status.HTTP_200_OK)
async def comunas(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[BarrioSchema]:
    barrios = ComunaCRUD.read_barrios(db, id_comuna=id, skip=skip, limit=limit)
    return barrios


@router.get("/{id}/tangaras", response_model=list[TangaraSchema], status_code=status.HTTP_200_OK)
async def comunas(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[TangaraSchema]:
    tangaras = ComunaCRUD.read_tangaras(db, id_comuna=id, skip=skip, limit=limit)
    return tangaras