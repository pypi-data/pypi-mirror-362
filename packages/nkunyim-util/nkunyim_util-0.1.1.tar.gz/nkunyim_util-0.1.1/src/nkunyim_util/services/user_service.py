import base64
import json
from typing import Optional
from django.conf import settings
from django.http import HttpRequest

from nkunyim_util.models.user_model import UserModel
from nkunyim_util.encryption.rsa_encryption import RSAEncryption
from nkunyim_util.api.nkunyim_api_client import NkunyimApiClient
from nkunyim_util.services.signals import user_data_updated

class UserService:
    
    def get(self, req: HttpRequest) -> Optional[UserModel]:      
        try:
            user = req.user
            if not user.is_authenticated:
                return None
            
            client = NkunyimApiClient(req=req, name=settings.IDENTITY_SERVICE)
            response = client.get(path=f"/api/users/me")
            if not response.ok:
                # log error
                return None
            
            json_data = response.json()
            result_data = dict(json_data)
            
            user_model = UserModel(**result_data)
                
            # Inform interested parties
            user_data_updated.send(sender=UserModel, instance=user_model)
            
            return user_model
        except:
            return None 
        
        
    def set(self, token: str) -> Optional[UserModel]:
        try:
            cipher_token = token[2:-1] # Cater for bytes str concatenation issue
            encryption = RSAEncryption()
            cipher_text = base64.b64decode(cipher_token)
            plain_text = encryption.decrypt(cipher_text=cipher_text)
            userinfo = json.loads(plain_text)
            user_data = dict(userinfo)
            return UserModel(**user_data)
        except Exception as ex:
            return None