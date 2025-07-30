from django.http import HttpRequest

from nkunyim_util.models.context_model import ContextModel
from nkunyim_util.services.access_service import AccessService
from nkunyim_util.services.app_service import AppService
from nkunyim_util.services.location_service import LocationService
from nkunyim_util.services.nation_service import NationService
from nkunyim_util.services.page_service import PageService
from nkunyim_util.services.user_agent_service import UserAgentService
from nkunyim_util.services.user_service import UserService


class ContextService:
    
    def __init__(self, req: HttpRequest) -> None:
        self.req = req
        
    
    def create(self) -> ContextModel:
        page_model = PageService(req=self.req)
        page_data = page_model.get()
        
        app_model = AppService(req=self.req, session_key=page_data.root)
        app_data = app_model.get()
        
        user_model = UserService()
        user_data = user_model.get(req=self.req)
    
        access_model = AccessService(req=self.req, session_key=page_data.root, application_id=app_data.id)
        access_data = access_model.get()
    
        location_model = LocationService(req=self.req, session_key=page_data.root)
        location_data = location_model.get()
        
        nation_model = NationService(req=self.req, session_key=page_data.root, code=location_data.country_code)
        nation_data = nation_model.get()
        
        user_agent_model = UserAgentService(req=self.req, session_key=page_data.root)
        user_agent_data = user_agent_model.get()
        
        data = {
            **app_data.__dict__,
            "page": page_data.__dict__,
            "user": user_data.__dict__,
            "uix": access_data.uix,
            "navs": access_data.navs,
            "role": access_data.role,
            "location": location_data.__dict__,
            "nation": nation_data.__dict__,
            "user_agent": user_agent_data.__dict__,
            "root": page_data.root
        }
        
        return ContextModel(**data)