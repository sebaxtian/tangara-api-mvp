from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.barrio import BarrioSchema, BarrioCreate, BarrioUpdate
from app.crud.barrio import BarrioCRUD
from app.schemas.tangara import TangaraSchema


router = APIRouter(
    prefix="/barrios",
    tags=["barrios"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=list[BarrioSchema], status_code=status.HTTP_200_OK)
async def barrios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[BarrioSchema]:
    barrios = BarrioCRUD.read_barrios(db, skip=skip, limit=limit)
    return barrios


@router.get("/{id}", response_model=BarrioSchema, status_code=status.HTTP_200_OK)
async def barrios(id: int, db: Session = Depends(get_db)) -> BarrioSchema:
    barrio = BarrioCRUD.read_barrio(db, id_barrio=id)
    if not barrio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return barrio


@router.post("/", response_model=BarrioSchema, status_code=status.HTTP_201_CREATED)
async def barrios(barrio: BarrioCreate, db: Session = Depends(get_db)) -> BarrioSchema:
    barrio = BarrioCRUD.create_barrio(db, barrio=barrio)
    return barrio


@router.put("/{id}", response_model=BarrioSchema, status_code=status.HTTP_200_OK)
async def barrios(id: int, barrio: BarrioUpdate, db: Session = Depends(get_db)) -> BarrioSchema:
    barrio = BarrioCRUD.update_barrio(db, id_barrio=id, barrio=barrio)
    if not barrio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return barrio


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def barrios(id: int, db: Session = Depends(get_db)) -> None:
    BarrioCRUD.delete_barrio(db, id_barrio=id)


@router.get("/{id}/tangaras", response_model=list[TangaraSchema], status_code=status.HTTP_200_OK)
async def barrios(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[TangaraSchema]:
    tangaras = BarrioCRUD.read_tangaras(db, id_barrio=id, skip=skip, limit=limit)
    return tangaras
