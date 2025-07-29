from typing import Union
from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS

from nkunyim_util.models.location_model import LocationModel

from .cache_manager import CacheManager, DEFAULT_CACHE_TIMEOUT
  

   
class LocationCache:

    def __init__(self, key: str) -> None:
        self.key = key
        self.cache = CacheManager(settings.LOCATION_CACHE if hasattr(settings, 'LOCATION_CACHE') else DEFAULT_CACHE_ALIAS)
        
    def set(self, model: LocationModel, timeout: int = DEFAULT_CACHE_TIMEOUT):
        self.cache.set(key=self.key, value=model, timeout=timeout)
        
    def get(self) -> Union[LocationModel, None]:
        return self.cache.get(key=self.key)
    
    def delete(self) -> None:
        self.cache.delete(key=self.key)
        
    def clear(self) -> None:
        self.cache.clear()
        
      