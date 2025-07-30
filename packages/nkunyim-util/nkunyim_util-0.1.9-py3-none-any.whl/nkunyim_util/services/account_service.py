from collections import defaultdict
from typing import List, Optional
from uuid import UUID

from django.conf import settings
from django.http import HttpRequest

from nkunyim_util.caches.account_cache import AccountCache
from nkunyim_util.models.account_model import AccountModel, MenuModel, NavModel
from nkunyim_util.api.nkunyim_api_client import NkunyimApiClient
from nkunyim_util.models.user_model import RoleModel
from nkunyim_util.services.session_service import SessionService


from .signals import access_data_updated


class AccountService:
    
    def __init__(self, req: HttpRequest, session_key: str, application_id: UUID) -> None:
        self.cache = AccountCache(key=f"acc.{session_key}")
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
        
        
    def _get_account_from_api(self) -> Optional[dict]:
        try:
            client = NkunyimApiClient(req=self.req, name=settings.MARKET_SERVICE)
            response = client.get(path=f"/api/accounts/menus/?application_id={self.application_id}")
            return dict(response.json()) if response.ok else None
        except:
            return None
        
        
    def _make(self) -> AccountModel:
        navs = None
        uix = dict(settings.NKUNYIM_UIX)
        account = self._get_account_from_api()
        if account and 'id' in account and account['id']:
            navs_uix = self._build_from_menus(menus=account['menus'])
            nui, navs = navs_uix
            uix.update(nui)

        else:
            account = {}
        
        role = account.get('role', None)
        if role and 'id' in role and role['id']:
            session_service = SessionService(req=self.req)
            user = session_service.get_user()
            if user :
                user.role = RoleModel(**role)
                session_service.set_user(user_model=user)
            
        model_data = {
            **account,
            'navs': navs,
            'uix': uix
        }
        access_model = AccountModel(**model_data)
        self.cache.set(model=access_model, timeout=60 * 60 * 24)
        
        # Inform interested parties
        access_data_updated.send(sender=AccountModel, instance=access_model)
        
        return access_model
            
    
    def get(self, refresh: bool = False) -> AccountModel:
        return self._make() if refresh else self.cache.get() or self._make()

