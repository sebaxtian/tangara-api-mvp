from functools import lru_cache

from config import Settings


# Dependency
@lru_cache()
def get_settings():
    return Settings()
