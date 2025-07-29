from typing import Optional
from django.http import HttpRequest

from nkunyim_util.models.logging_model import LoggingModel
from nkunyim_util.services.location_service import LocationService
from nkunyim_util.services.page_service import PageService
from nkunyim_util.services.user_agent_service import UserAgentService


class LoggingService:
    
    def __init__(self, req: HttpRequest) -> None:
        self.req = req


    def get(self, xan: str, service_name: Optional[str] = None) -> LoggingModel:
        page_model = PageService(req=self.req)
        page_data = page_model.get()
        
        if not service_name:
            service_name = page_data.subdomain
            
        location_model = LocationService(req=self.req, session_key=page_data.root)
        location_data = location_model.get()
        
        user_agent_model = UserAgentService(req=self.req, session_key=page_data.root)
        user_agent_data = user_agent_model.get()
        
        logging_model = LoggingModel(
            xan=xan,
            service_name=service_name,
            location=location_data,
            user_agent=user_agent_data
        )
        
        return logging_model