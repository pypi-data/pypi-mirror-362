from collections import defaultdict
from typing import List, Optional
from uuid import UUID

from django.conf import settings
from django.http import HttpRequest

from nkunyim_util.caches.access_cache import AccessCache
from nkunyim_util.models.access_model import AccessModel, MenuModel, NavModel
from nkunyim_util.api.nkunyim_api_client import NkunyimApiClient


from .signals import access_data_updated


class AccessService:
    
    def __init__(self, req: HttpRequest, session_key: str, application_id: UUID) -> None:
        self.cache = AccessCache(key=f"acc.{session_key}")
        self.application_id = str(application_id)
        self.req = req


    def _build_from_menus(self, menus: List[dict]) -> tuple[dict[str, str], List[NavModel]] :
        env = "dev"
        uix = {}
        menus_dict = defaultdict(List[MenuModel])

        for menu in menus:
            node = menu['node']
            module = menu['module']
            menu_data = {
                '_id': menu['id'],
                'node': node,
                'seq': menu['seq'],
                **{key: module[key] for key in (
                    'id', 'name', 'title', 'caption', 'icon', 'path', 'route', 'colour', 'tags'
                )}
            }
            items = menu['items']

            module_name = str(module['name']).title()
            module_path = str(module['path']).lower()
            
            uix[f"{module_name}Page"] = f"./{module_path}/home.{env}"

            menu_data['items'] = []
            for item in items:
                page = item['page']
                uix[f"{module_name}{str(page['name']).title()}Page"] = f"./{module_path}/{str(page['path']).lower()}.{env}"
                item_data = {
                    '_id': menu['id'],
                    'seq': menu['seq'],
                    **{key: page[key] for key in (
                        'id', 'name', 'title', 'caption', 'icon', 'path', 'route', 'tags'
                    )}
                }
                menu_data['items'].append(item_data)
                
            if node in {"dashboard", "modules", "account", "system"}:
                menus_dict[node].append(MenuModel(**menu_data))

        navs = [
            NavModel(node=str(nodex).title(), menus=menux)
            for nodex, menux in menus_dict.items()
        ]

        return uix, navs
        
        
    def _get_menus_from_api(self, access_id: UUID) -> Optional[List[dict]]:
        try:
            client = NkunyimApiClient(req=self.req, name=settings.MARKET_SERVICE)
            response = client.get(path=f"/api/menus/account/?account_id={str(access_id)}")
            return response.json() if response.ok else None
        except:
            return None
        
        
    def _get_access_from_api(self) -> Optional[dict]:
        try:
            client = NkunyimApiClient(req=self.req, name=settings.ACCOUNT_SERVICE)
            response = client.get(path=f"/api/accesses/account/?application_id={self.application_id}")
            return dict(response.json()) if response.ok else None
        except:
            return None
        
        
    def _make(self) -> AccessModel:
        id = name = tags = role = navs = None
        uix = dict(settings.NKUNYIM_UIX)
        access = self._get_access_from_api()
        if access and 'id' in access:
            id = access['id']
            name = access['name']
            tags = access['tags']
            role = access['role']
            menus = self._get_menus_from_api(UUID(access['id']))
            if menus:
                navs_uix = self._build_from_menus(menus=menus)
                nui, navs = navs_uix
                uix.update(nui)
            
        model_data = {
            'id': id,
            'name': name,
            'tags': tags,
            'role': role,
            'navs': navs,
            'uix': uix
        }
        access_model = AccessModel(**model_data)
        self.cache.set(model=access_model, timeout=60 * 60 * 24)
        
        # Inform interested parties
        access_data_updated.send(sender=AccessModel, instance=access_model)
        
        return access_model
            
    
    def get(self, refresh: bool = False) -> AccessModel:
        return self._make() if refresh else self.cache.get() or self._make()

