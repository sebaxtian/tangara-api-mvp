from fastapi import Depends, FastAPI

from datetime import timedelta
from fastapi_cache.decorator import cache
from redis import Redis
from redis.exceptions import ConnectionError

from app.config import Settings
from app.dependencies.database import get_db
from app.dependencies.settings import get_settings
from app.dependencies.redis import get_redis
from app.routers import comunas, barrios, veredas, sectores, areasexp, areaspro, tangaras, lugares, pm25


app = FastAPI(
    dependencies=[Depends(get_db), Depends(get_settings), Depends(get_redis)]
)


@app.on_event("startup")
async def startup(conn: Redis = get_redis()):
    print("CONNECT_BEGIN: Attempting to connect to Redis server...")
    try:
        print(f"Ping successful: {await conn.ping()}")
        print("CONNECT_SUCCESS: Redis client is connected to server.")
    except ConnectionError:
        print("CONNECT_FAIL: Redis server not response.")


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
