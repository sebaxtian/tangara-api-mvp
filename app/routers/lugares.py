from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
import io

from dependencies.db import get_db
from schemas.lugares import LugaresSchema
from crud.lugares import LugaresCRUD


router = APIRouter(
    prefix="/lugares",
    tags=["lugares"],
    dependencies=[Depends(get_db)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}}
)


@router.get("/", response_model=list[LugaresSchema], status_code=status.HTTP_200_OK)
async def lugares(format: str = "json", db: Session = Depends(get_db)) -> list[LugaresSchema]:
    lugares = LugaresCRUD.read_lugares(db)
    if format == "csv":
        df = pd.DataFrame(data=lugares)
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    return lugares
