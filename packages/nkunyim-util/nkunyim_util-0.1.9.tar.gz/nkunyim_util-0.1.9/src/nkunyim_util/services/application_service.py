from typing import Optional
from django.conf import settings
from django.http import HttpRequest

from nkunyim_util.models.application_model import ApplicationModel
from nkunyim_util.caches.application_cache import ApplicationCache
from nkunyim_util.api.nkunyim_api_client import NkunyimApiClient


from .signals import app_data_updated


class ApplicationService:
    
    def __init__(self, req: HttpRequest, session_key: str) -> None:
        self.cache = ApplicationCache(key=f"app.{session_key}")
        self.req = req


    def _get_from_api(self) -> Optional[dict]:
        try:
            modules = []
            domain = '.'.join(self.req.get_host().rsplit('.', 2)[-2:]).lower()
            client = NkunyimApiClient(req=self.req, name=settings.MARKET_SERVICE)
            response = client.get(path=f"/api/applications/session/?domain={domain}")
            if not response.ok:
                # log error
                return None
            
            json_data = response.json()
            application = json_data['application']
            packets = json_data.get('packets', None)
            if packets:
                for packet in packets:
                    modules.append({
                        "id": packet['module']['id'],
                        "name": packet['module']['name'],
                        "title": packet['module']['title'],
                        "version": packet['version']['code'],
                    })

            return {
                **application,
                "modules": modules,
            }
        except:
            return None


    def _make(self) -> ApplicationModel:
        model_data = self._get_from_api()
        if not model_data:
            model_data = dict(settings.NKUNYIM_DEFAULT_APP)
    
        app_model = AppModel(**model_data) # type: ignore
        self.cache.set(model=app_model, timeout=60 * 60 * 24)
        
        # Inform interested parties
        app_data_updated.send(sender=ApplicationModel, instance=app_model)
        
        return app_model
    
    
    def get(self) -> ApplicationModel:
        return self.cache.get() or self._make()
    