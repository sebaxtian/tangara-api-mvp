from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
import io

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from datetime import timedelta

from app.dependencies.database import get_db
from app.schemas.lugares import LugaresSchema
from app.crud.lugares import LugaresCRUD


router = APIRouter(
    prefix="/lugares",
    tags=["lugares"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=list[LugaresSchema], status_code=status.HTTP_200_OK)
async def lugares(format: str = "json", db: Session = Depends(get_db)) -> list[LugaresSchema]:
    lugares = await FastAPICache.get_backend().get("lugares")
    if not lugares:
        lugares = LugaresCRUD.read_lugares(db)
        await FastAPICache.get_backend().set("lugares", lugares, expire=timedelta(days=30).seconds)
    if format == "csv":
        df = pd.DataFrame(data=lugares)
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    return lugares
