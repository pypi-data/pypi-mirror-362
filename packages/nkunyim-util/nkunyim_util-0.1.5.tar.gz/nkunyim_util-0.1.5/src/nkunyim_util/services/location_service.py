from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpRequest

from nkunyim_util.caches.location_cache import LocationCache
from nkunyim_util.models.location_model import LocationModel

 


class LocationService:
    
    FALLBACK_IP = "154.160.22.132"
    PRIVATE_IP_PREFIXES = ("192.168.",)
    LOCALHOST_SUFFIXES = (".0.0.1",)

    def __init__(self, req: HttpRequest, session_key: str) -> None:
        self.cache = LocationCache(key=f"loc.{session_key}")
        self.user_ip = self._extract_ip(req)
        self.req = req
    
    def _extract_ip(self, request: HttpRequest) -> str:
        ip = (
            request.META.get("HTTP_X_FORWARDED_FOR")
            or request.META.get("HTTP_X_REAL_IP")
            or request.META.get("REMOTE_ADDR", "")
        ).split(",")[0].strip()

        if ip.startswith(self.PRIVATE_IP_PREFIXES) or any(ip.endswith(suffix) for suffix in self.LOCALHOST_SUFFIXES):
            return self.FALLBACK_IP
        return ip
    
    def _make(self) -> LocationModel:
        geoip = GeoIP2()
        data = geoip.city(self.user_ip)
        data['user_ip'] = self.user_ip
        location_model = LocationModel(**data)
        self.cache.set(model=location_model, timeout=60 * 60 * 24)
        
        return location_model
        
    def get(self) -> LocationModel:
        return self.cache.get() or self._make()
    
    