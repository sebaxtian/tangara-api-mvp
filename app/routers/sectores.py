from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.sector import SectorSchema, SectorCreate, SectorUpdate
from app.crud.sector import SectorCRUD
from app.schemas.tangara import TangaraSchema


router = APIRouter(
    prefix="/sectores",
    tags=["sectores"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=list[SectorSchema], status_code=status.HTTP_200_OK)
async def sectores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[SectorSchema]:
    sectores = SectorCRUD.read_sectores(db, skip=skip, limit=limit)
    return sectores


@router.get("/{id}", response_model=SectorSchema, status_code=status.HTTP_200_OK)
async def sectores(id: int, db: Session = Depends(get_db)) -> SectorSchema:
    sector = SectorCRUD.read_sector(db, id_sector=id)
    if not sector:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return sector


@router.post("/", response_model=SectorSchema, status_code=status.HTTP_201_CREATED)
async def sectores(sector: SectorCreate, db: Session = Depends(get_db)) -> SectorSchema:
    sector = SectorCRUD.create_sector(db, sector=sector)
    return sector


@router.put("/{id}", response_model=SectorSchema, status_code=status.HTTP_200_OK)
async def sectores(id: int, sector: SectorUpdate, db: Session = Depends(get_db)) -> SectorSchema:
    sector = SectorCRUD.update_sector(db, id_sector=id, sector=sector)
    if not sector:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return sector


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def sectores(id: int, db: Session = Depends(get_db)) -> None:
    SectorCRUD.delete_sector(db, id_sector=id)


@router.get("/{id}/tangaras", response_model=list[TangaraSchema], status_code=status.HTTP_200_OK)
async def sectores(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[TangaraSchema]:
    tangaras = SectorCRUD.read_tangaras(db, id_sector=id, skip=skip, limit=limit)
    return tangaras
