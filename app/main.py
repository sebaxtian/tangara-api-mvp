from fastapi import Depends, FastAPI

from dependencies.database import get_db
from routers import comunas, barrios, veredas, sectores, areasexp


app = FastAPI(
    dependencies=[Depends(get_db)]
)


app.include_router(comunas.router)
app.include_router(barrios.router)
app.include_router(veredas.router)
app.include_router(sectores.router)
app.include_router(areasexp.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
