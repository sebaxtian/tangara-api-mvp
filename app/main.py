from fastapi import Depends, FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from starlette.responses import JSONResponse
from datetime import timedelta

from app.config import Settings
from app.dependencies.database import get_db
from app.dependencies.settings import get_settings
from app.dependencies.mem_cache import create_mem_cache
from app.routers import comunas, barrios, veredas, sectores, areasexp, areaspro, tangaras, lugares, pm25


app = FastAPI(
    dependencies=[Depends(get_db), Depends(get_settings)],
    on_startup=[create_mem_cache]
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
@cache(namespace="root", expire=timedelta(minutes=5).seconds)
async def root(settings: Settings = Depends(get_settings)) -> JSONResponse:
    return JSONResponse({"message": settings.app_name, "environment": settings.env})


@app.get("/clear")
async def clear():
    await FastAPICache.clear(namespace="root")
