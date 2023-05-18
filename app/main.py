from fastapi import Depends, FastAPI

from dependencies.database import get_db
from routers import comuna


app = FastAPI(
    dependencies=[Depends(get_db)]
)


app.include_router(comuna.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
