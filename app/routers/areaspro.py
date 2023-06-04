from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.areapro import AreaProSchema, AreaProCreate, AreaProUpdate
from app.crud.areapro import AreaProCRUD
from app.schemas.tangara import TangaraSchema


router = APIRouter(
    prefix="/areaspro",
    tags=["areaspro"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=list[AreaProSchema], status_code=status.HTTP_200_OK)
async def areaspro(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[AreaProSchema]:
    areaspro = AreaProCRUD.read_areaspro(db, skip=skip, limit=limit)
    return areaspro


@router.get("/{id}", response_model=AreaProSchema, status_code=status.HTTP_200_OK)
async def areaspro(id: int, db: Session = Depends(get_db)) -> AreaProSchema:
    areapro = AreaProCRUD.read_areapro(db, id_areapro=id)
    if not areapro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return areapro


@router.post("/", response_model=AreaProSchema, status_code=status.HTTP_201_CREATED)
async def areaspro(areapro: AreaProCreate, db: Session = Depends(get_db)) -> AreaProSchema:
    areapro = AreaProCRUD.create_areapro(db, areapro=areapro)
    return areapro


@router.put("/{id}", response_model=AreaProSchema, status_code=status.HTTP_200_OK)
async def areaspro(id: int, areapro: AreaProUpdate, db: Session = Depends(get_db)) -> AreaProSchema:
    areapro = AreaProCRUD.update_areapro(db, id_areapro=id, areapro=areapro)
    if not areapro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return areapro


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def areaspro(id: int, db: Session = Depends(get_db)) -> None:
    AreaProCRUD.delete_areapro(db, id_areapro=id)


@router.get("/{id}/tangaras", response_model=list[TangaraSchema], status_code=status.HTTP_200_OK)
async def areaspro(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[TangaraSchema]:
    tangaras = AreaProCRUD.read_tangaras(db, id_areapro=id, skip=skip, limit=limit)
    return tangaras
