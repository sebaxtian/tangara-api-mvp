from fastapi import Depends, FastAPI

from app.config import Settings
from app.dependencies.database import get_db
from app.dependencies.settings import get_settings
from app.routers import comunas, barrios, veredas, sectores, areasexp, areaspro, tangaras, lugares, pm25


app = FastAPI(
    dependencies=[Depends(get_db), Depends(get_settings)]
)


app.include_router(comunas.router)
app.include_router(barrios.router)
app.include_router(veredas.router)
app.include_router(sectores.router)
app.include_router(areasexp.router)
app.include_router(areaspro.router)
app.include_router(tangaras.router)
app.include_router(lugares.router)
app.include_router(pm25.router)


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"message": settings.app_name, "environment": settings.env}
