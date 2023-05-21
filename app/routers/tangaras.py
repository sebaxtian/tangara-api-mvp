from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from dependencies.db import get_db
from schemas.tangara import TangaraSchema, TangaraCreate, TangaraUpdate
from crud.tangara import TangaraCRUD


router = APIRouter(
    prefix="/tangaras",
    tags=["tangaras"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=list[TangaraSchema], status_code=status.HTTP_200_OK)
async def tangaras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[TangaraSchema]:
    tangaras = TangaraCRUD.read_tangaras(db, skip=skip, limit=limit)
    return tangaras


@router.get("/{id}", response_model=TangaraSchema, status_code=status.HTTP_200_OK)
async def tangaras(id: int, db: Session = Depends(get_db)) -> TangaraSchema:
    tangara = TangaraCRUD.read_tangara(db, id_tangara=id)
    if not tangara:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return tangara


@router.post("/", response_model=TangaraSchema, status_code=status.HTTP_201_CREATED)
async def tangaras(tangara: TangaraCreate, db: Session = Depends(get_db)) -> TangaraSchema:
    tangara = TangaraCRUD.create_tangara(db, tangara=tangara)
    return tangara


@router.put("/{id}", response_model=TangaraSchema, status_code=status.HTTP_200_OK)
async def tangaras(id: int, tangara: TangaraUpdate, db: Session = Depends(get_db)) -> TangaraSchema:
    tangara = TangaraCRUD.update_tangara(db, id_tangara=id, tangara=tangara)
    if not tangara:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return tangara


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def tangaras(id: int, db: Session = Depends(get_db)) -> None:
    TangaraCRUD.delete_tangara(db, id_tangara=id)
