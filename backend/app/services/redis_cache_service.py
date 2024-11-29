from typing import List, Optional, Union
from app.services.redis_interface import CacheService
from app.services.redis_client import clear_cache, set_data, get_data

class RedisCacheService(CacheService):
    def set_data(self, key: str, value: list) -> None:
        """Store data in Redis"""
        set_data(key, value)

    def get_data(self, key: str) -> Optional[list]:
        """Retrieve data from Redis"""
        return get_data(key)
    
    def clear_cache(self) -> None:
        clear_cache(self)