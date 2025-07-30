
from typing import Optional
from django.conf import settings
from django.http import HttpRequest

from nkunyim_util.models.user_model import UserModel
from nkunyim_util.api.nkunyim_api_client import NkunyimApiClient
from nkunyim_util.services.session_service import SessionService
from nkunyim_util.services.signals import user_data_updated

class UserService:
    
    def __init__(self, req: HttpRequest) -> None:
        self.req = req
        
        
    def api(self, token: str) -> Optional[UserModel]:
        ...
    
    def app(self) -> Optional[UserModel]:      
        try:
            session_service = SessionService(req=self.req)
            if not session_service.has_lifetime:
                return None
            
            user_model = session_service.get_user()
            if user_model:
                return user_model
            
            client = NkunyimApiClient(req=self.req, name=settings.IDENTITY_SERVICE_NAME)
            response = client.get(path="/api/users/me")
            user_data = response.json() if response.ok else None  
            if not user_data:
                return None
            
            if not ('id' in user_data and user_data['id']):
                return None
            
            user_model = UserModel(**user_data)
            session_service.set_user(user_model=user_model)
            
            # Inform interested parties
            user_data_updated.send(sender=UserModel, instance=user_model)
            
            return user_model
        except:
            return None 
        
