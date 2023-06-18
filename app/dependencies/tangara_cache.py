from fastapi import FastAPI

import hashlib
from typing import Callable, Optional

from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from redis.exceptions import ConnectionError

from contextlib import asynccontextmanager


from app.dependencies.settings import get_settings


def api_key_builder(
    func: Callable,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
) -> str:
    from fastapi_cache import FastAPICache

    # SOLUTION: https://github.com/long2ice/fastapi-cache/issues/26
    #print("kwargs.items():", kwargs.items())
    arguments = {}
    for key, value in kwargs.items():
        if key != 'db':
            arguments[key] = value
    #print("request:", request, "request.base_url:", request.base_url, "request.url:", request.url)
    arguments['url'] = request.url
    #print("arguments:", arguments)

    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    cache_key = (
        prefix
        + hashlib.md5(  # nosec:B303
            f"{func.__module__}:{func.__name__}:{args}:{arguments}".encode()
        ).hexdigest()
    )
    return cache_key


# Dependency
def create_mem_cache():
    print("\nFastAPICache: create_mem_cache ...")
    FastAPICache.init(InMemoryBackend(), prefix="tangara-cache", key_builder=api_key_builder)
    print("FastAPICache: create_mem_cache DONE!\n")

# Dependency
async def create_redis_cache():
    print("\nFastAPICache: create_redis_cache ...")
    redis = aioredis.from_url(get_settings().url_redis)
    FastAPICache.init(RedisBackend(redis), prefix="tangara-cache", key_builder=api_key_builder)
    try:
        print(f"Ping successful: {await redis.ping()}")
        print("CONNECT_SUCCESS: Redis client is connected to server.")
        print("FastAPICache: create_redis_cache DONE!\n")
    except ConnectionError:
        print("\nCONNECT_FAIL: Redis server not response.")
        FastAPICache.reset()
        create_mem_cache()


# Dependency
@asynccontextmanager
async def create_cache(app: FastAPI):
    # Developer mode
    if get_settings().env == "dev":
        await create_redis_cache()
    # Production mode
    yield
