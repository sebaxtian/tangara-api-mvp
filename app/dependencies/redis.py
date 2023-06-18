from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import redis.asyncio as redis
from redis import Redis

from app.config import Settings
from app.dependencies.settings import get_settings


def get_redis() -> Redis:
    settings: Settings = get_settings()
    conn = redis.from_url(url=settings.redis_server)
    FastAPICache.init(RedisBackend(conn), prefix="tangara-cache")
    return conn
