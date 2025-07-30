from django.core.cache import DEFAULT_CACHE_ALIAS,  caches


DEFAULT_CACHE_TIMEOUT: int = 60 * 60 * 24


class CacheManager:
    """
    A simple cache manager to handle caching operations.
    """

    def __init__(self, cache_alias: str = DEFAULT_CACHE_ALIAS) -> None:
        self.cache = caches[cache_alias]


    def set(self, key, value, timeout=None):
        """
        Set a value in the cache.
        
        :param key: The key under which the value is stored.
        :param value: The value to store.
        :param timeout: The time in seconds before the cache expires.
        """
        if self.cache:
            self.cache.set(key, value, timeout)


    def get(self, key):
        """
        Get a value from the cache.
        
        :param key: The key of the cached value.
        :return: The cached value or None if not found.
        """
        if self.cache:
            return self.cache.get(key)
        return None


    def delete(self, key):
        """
        Delete a value from the cache.
        
        :param key: The key of the cached value to delete.
        """
        if self.cache:
            self.cache.delete(key)
            
            
    def clear(self):
        """
        Clear the entire cache.
        """
        if self.cache:
            self.cache.clear()
            
     