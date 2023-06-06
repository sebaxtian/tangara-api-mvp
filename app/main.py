from fastapi import Depends, FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from datetime import timedelta

from app.config import Settings
from app.dependencies.database import get_db
from app.dependencies.settings import get_settings
from app.routers import comunas, barrios, veredas, sectores, areasexp, areaspro, tangaras, lugares, pm25


app = FastAPI(
    dependencies=[Depends(get_db), Depends(get_settings)]
)


@app.on_event("startup")
def startup(settings: Settings = get_settings()):
    print("CONNECT_BEGIN: Attempting to connect to Redis server...")
    redis = aioredis.from_url(settings.redis_server)
    FastAPICache.init(RedisBackend(redis), prefix="tangara-cache")
    print("CONNECT_SUCCESS: Redis client is connected to server.")


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
@cache(expire=timedelta(minutes=5))
async def root(settings: Settings = Depends(get_settings)):
    return {"message": settings.app_name, "environment": settings.env}
