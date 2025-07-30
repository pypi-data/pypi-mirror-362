from typing import Union
from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS

from nkunyim_util.models.application_model import ApplicationModel

from .cache_manager import CacheManager, DEFAULT_CACHE_TIMEOUT


    
class ApplicationCache:

    def __init__(self, key: str) -> None:
        self.key = key
        self.cache = CacheManager(settings.APPLICATION_CACHE if hasattr(settings, 'APPLICATION_CACHE') else DEFAULT_CACHE_ALIAS)
        
    def set(self, model: ApplicationModel, timeout: int = DEFAULT_CACHE_TIMEOUT):
        self.cache.set(key=self.key, value=model, timeout=timeout)
        
    def get(self) -> Union[ApplicationModel, None]:
        return self.cache.get(key=self.key)
    
    def delete(self) -> None:
        self.cache.delete(key=self.key)
        
    def clear(self) -> None:
        self.cache.clear()

   