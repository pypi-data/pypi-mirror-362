from typing import Union
from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS

from nkunyim_util.models.access_model import AccessModel

from .cache_manager import CacheManager, DEFAULT_CACHE_TIMEOUT
  

   
class AccessCache:

    def __init__(self, key: str) -> None:
        self.key = key
        self.cache = CacheManager(settings.ACCESS_CACHE if hasattr(settings, 'ACCESS_CACHE') else DEFAULT_CACHE_ALIAS)
        
    def set(self, model: AccessModel, timeout: int = DEFAULT_CACHE_TIMEOUT):
        self.cache.set(key=self.key, value=model, timeout=timeout)
        
    def get(self) -> Union[AccessModel, None]:
        return self.cache.get(key=self.key)
    
    def delete(self) -> None:
        self.cache.delete(key=self.key)
        
    def clear(self) -> None:
        self.cache.clear()
        
      