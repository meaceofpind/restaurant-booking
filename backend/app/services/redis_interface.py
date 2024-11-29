from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

class CacheService(ABC):
    @abstractmethod
    def set_data(self, key: str, value: list) -> None:
        """Store data in cache"""
        pass

    @abstractmethod
    def get_data(self, key: str) -> Optional[list]:
        """Retrieve data from cache"""
        pass

    @abstractmethod
    def clear_cache(self) -> None:
        """Retrieve data from cache"""
        pass
