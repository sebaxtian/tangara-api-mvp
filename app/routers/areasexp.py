from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from datetime import timedelta

from app.dependencies.database import get_db
from app.schemas.areaexp import AreaExpSchema, AreaExpCreate, AreaExpUpdate, AreaExpPaginationSchema
from app.crud.areaexp import AreaExpCRUD
from app.schemas.tangara import TangaraPaginationSchema


router = APIRouter(
    prefix="/areasexp",
    tags=["areasexp"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=AreaExpPaginationSchema, status_code=status.HTTP_200_OK)
@cache(namespace="areasexp", expire=timedelta(days=30))
async def areasexp(skip: int = 0, limit: int = None, db: Session = Depends(get_db)) -> AreaExpPaginationSchema:
    areasexp = AreaExpCRUD.read_areasexp(db, skip=skip, limit=limit)
    return areasexp


@router.get("/{id}", response_model=AreaExpSchema, status_code=status.HTTP_200_OK)
@cache(namespace="areasexp", expire=timedelta(days=30))
async def areasexp(id: int, db: Session = Depends(get_db)) -> AreaExpSchema:
    areaexp = AreaExpCRUD.read_areaexp(db, id_areaexp=id)
    if not areaexp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return areaexp


@router.post("/", response_model=AreaExpSchema, status_code=status.HTTP_201_CREATED)
async def areasexp(areaexp: AreaExpCreate, db: Session = Depends(get_db)) -> AreaExpSchema:
    areaexp = AreaExpCRUD.create_areaexp(db, areaexp=areaexp)
    #await FastAPICache.clear(namespace="areasexp")
    return areaexp


@router.put("/{id}", response_model=AreaExpSchema, status_code=status.HTTP_200_OK)
async def areasexp(id: int, areaexp: AreaExpUpdate, db: Session = Depends(get_db)) -> AreaExpSchema:
    areaexp = AreaExpCRUD.update_areaexp(db, id_areaexp=id, areaexp=areaexp)
    if not areaexp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #await FastAPICache.clear(namespace="areasexp")
    return areaexp


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def areasexp(id: int, db: Session = Depends(get_db)) -> None:
    AreaExpCRUD.delete_areaexp(db, id_areaexp=id)
    #await FastAPICache.clear(namespace="areasexp")


@router.get("/{id}/tangaras", response_model=TangaraPaginationSchema, status_code=status.HTTP_200_OK)
@cache(namespace="areasexp", expire=timedelta(days=30))
async def areasexp(id: int, skip: int = 0, limit: int = None, db: Session = Depends(get_db)) -> TangaraPaginationSchema:
    tangaras = AreaExpCRUD.read_tangaras(db, id_areaexp=id, skip=skip, limit=limit)
    return tangaras
