from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
import io

from fastapi_cache import FastAPICache
from datetime import timedelta
import json

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
    from fastapi_cache.backends.redis import RedisBackend
    #print("isinstance(FastAPICache.get_backend(), RedisBackend):", isinstance(FastAPICache.get_backend(), RedisBackend))
    if not isinstance(FastAPICache.get_backend(), RedisBackend) and format == "json":
        return LugaresCRUD.read_lugares(db)
    if not isinstance(FastAPICache.get_backend(), RedisBackend) and format == "csv":
        df = pd.DataFrame()
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    
    # Cache
    lugares = await FastAPICache.get_backend().get("lugares")

    # TODO: Add to Headers, cache-control max-age=*

    if not lugares:
        lugares = json.dumps(LugaresCRUD.read_lugares(db))
        await FastAPICache.get_backend().set("lugares", lugares, expire=timedelta(days=30))
    if format == "csv":
        lugares = json.loads(lugares)
        df = pd.DataFrame(data=lugares)
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    
    return json.loads(lugares)
