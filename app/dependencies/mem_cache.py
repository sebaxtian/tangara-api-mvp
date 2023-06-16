from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
#from fastapi_cache.backends.redis import RedisBackend
#from redis import asyncio as aioredis


# Dependency
def create_mem_cache():
    print("FastAPICache: create_mem_cache ...")
    FastAPICache.init(InMemoryBackend(), prefix="tangara-cache")
    #redis = aioredis.from_url("redis://127.0.0.1:6379")
    #FastAPICache.init(RedisBackend(redis), prefix="tangara-cache")
    print("FastAPICache: create_mem_cache DONE!")
