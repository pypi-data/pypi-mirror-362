from typing import Optional
from django.conf import settings
from django.http import HttpRequest

from nkunyim_util.models.app_model import AppModel
from nkunyim_util.caches.app_cache import AppCache
from nkunyim_util.api.nkunyim_api_client import NkunyimApiClient


from .signals import app_data_updated


class AppService:
    
    def __init__(self, req: HttpRequest, session_key: str) -> None:
        self.cache = AppCache(key=f"app.{session_key}")
        self.req = req


    def _get_from_api(self) -> Optional[AppModel]:
        try:
            domain = '.'.join(self.req.get_host().rsplit('.', 2)[-2:]).lower()
            client = NkunyimApiClient(req=self.req, name=settings.MARKET_SERVICE)
            response = client.get(path=f"/api/applications/?domain={domain}")
            if not response.ok:
                # log error
                return None
            
            json_data = response.json()
            result_data = dict(json_data).get("data", [None])
            model_data = result_data[0]

            return model_data
        except:
            return None


    def _make(self) -> AppModel:
        model_data = self._get_from_api()
        if not model_data:
            model_data = dict(settings.NKUNYIM_DEFAULT_APP)
    
        app_model = AppModel(**model_data) # type: ignore
        self.cache.set(model=app_model, timeout=60 * 60 * 24)
        
        # Inform interested parties
        app_data_updated.send(sender=AppModel, instance=app_model)
        
        return app_model
    
    
    def get(self) -> AppModel:
        return self.cache.get() or self._make()
    