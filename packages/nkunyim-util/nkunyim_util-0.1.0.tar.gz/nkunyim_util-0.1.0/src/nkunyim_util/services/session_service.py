from datetime import datetime
from typing import Optional
from django.http import HttpRequest

from nkunyim_util.models.session_model import SessionModel, TokenModel
from nkunyim_util.models.user_model import UserModel
from nkunyim_util.services.user_service import UserService


class SessionService:
    
    def __init__(self, req: HttpRequest) -> None:
        self.req = req
    
    
    def _key(self) -> str:
        parts = self.req.get_host().lower().split('.')
        if len(parts) >= 2:
            domain = '.'.join(parts[-2:])
            subdomain = parts[-3] if len(parts) > 2 else "www"
            return f"{subdomain}.{domain}"
        return "www.localhost"
    
    
    def set(self, model: SessionModel) -> None:
        self.req.session[self._key()] = model.model_dump()
        self.req.session.modified = True
        
        
    def get(self) -> Optional[SessionModel]:
        key = self._key()
        if not bool(key in self.req.session):
            return None

        session = self.req.session[key]
        return SessionModel(**session)
    
    
    def clear(self) -> None:
        self.req.session.clear()
        self.req.session.flush()
    
    
    def get_user(self) -> Optional[UserModel]:
        session_model = self.get()
        if session_model:
            return session_model.user
        
        
    def set_user(self) -> None:
        user_service = UserService()
        user_model = user_service.get(req=self.req)
        if user_model:
            session_model = self.get()
            if session_model:
                session_model.user = user_model
            else:
                 session_model = SessionModel(user=user_model, token=None)
                
            self.set(model=session_model)
            
        
    def get_token(self) -> Optional[TokenModel]:
        session_model = self.get()
        if session_model:
            return session_model.token
            
        
    def set_token(self, token_model: TokenModel) -> None:
        session_model = self.get()
        if session_model:
            session_model.token = token_model
        else:
            session_model = SessionModel(user=None, token=token_model)
            
        self.set(model=session_model)
        
    
    @property
    def lifetime(self) -> Optional[int]:
        token = self.get_token()
        if not token:
            return None
        current_datetime = datetime.now()
        time_difference = token.expires_at - current_datetime
        difference_in_seconds = time_difference.total_seconds()
        return int(difference_in_seconds)


    @property
    def is_authenticated(self) -> bool:
        user_model = self.get_user()
        return bool (user_model and user_model.id and self.lifetime  and self.lifetime > 0)

