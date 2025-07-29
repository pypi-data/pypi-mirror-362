
from rest_framework import HTTP_HEADER_ENCODING, authentication

from nkunyim_util.services.user_service import UserService



class JWTAuthentication(authentication.BaseAuthentication):
    
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
                            
        self.authentication_headers = ["JWT", "Bearer", ]
        self.www_authenticate_realm = 'api' 


    def authenticate_header(self, request): # type: ignore
        return '{0} realm="{1}"'.format(
            self.authentication_headers[0],
            self.www_authenticate_realm,
        )
        
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
                
        if isinstance(header, bytes):
            header = header.decode("utf-8") 
        
        token = self.get_raw_token(header)
        if token is None:
            return None
        
        user_service = UserService()
        user_model = user_service.set(token=token)
        if not user_model:
            return None
        
        # Return Auth Credentials
        return (user_model, None)


    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get('HTTP_AUTHORIZATION', None)
        if header is None:
            return None

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header
    
    
    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in self.authentication_headers:
            # Assume the header does not contain a JSON web token
            return None
        
        if len(parts) != 2:
            return None

        return parts[1]
    
   
    