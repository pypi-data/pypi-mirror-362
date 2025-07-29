import base64
import logging
import json
import requests
from django.conf import settings
from django.http import HttpRequest

from nkunyim_util.encryption.rsa_encryption import RSAEncryption
from nkunyim_util.logging.logging_command import LOG_TYPE_API
from nkunyim_util.logging.logging_handler import LoggingHandler
from nkunyim_util.services.logging_service import LoggingService


# Get a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# User handler
logging_handler = LoggingHandler()
logger.addHandler(logging_handler)

API_LOGGING_URL_KEY = "uri"
API_LOGGING_HEADERS_KEY = "headers"
API_LOGGING_BODY_KEY = "body"
API_LOGGING_METHOD_KEY = "method"
API_LOGGING_STATUS_KEY = "status"


class NkunyimApiClient:
    def __init__(self, req: HttpRequest, name: str) -> None:
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.req = req
        self.name = name.upper()
        self._init_base_url()
        self._init_headers()


    def _init_base_url(self) -> None:
        try:
            base_url = str(settings.NKUNYIM_SERVICES[self.name])
            self.base_url = base_url.rstrip('/')
        except KeyError:
            raise Exception(f"Service configuration '{self.name}' is not defined in settings.")


    def _init_headers(self) -> None:
        encryption = RSAEncryption()
        self._add_xan_authorization_header(encryption)
        self._add_jwt_authorization_header(encryption)


    def _add_xan_authorization_header(self, encryption: RSAEncryption) -> None:
        encrypted = encryption.encrypt(plain_text=self.name, name=self.name)
        token = base64.b64encode(encrypted).decode('utf-8')
        self.headers['Xan-Authorization'] = token


    def _add_jwt_authorization_header(self, encryption: RSAEncryption) -> None:
        user = self.req.user
        if user and user.is_authenticated:
            encrypted = encryption.encrypt(plain_text=json.dumps(user), name=self.name)
            token = base64.b64encode(encrypted).decode('utf-8')
            self.headers['Authorization'] = f'JWT {token}'


    def _build_url(self, path: str) -> str:
        base = self.base_url
        if not base.endswith('/api'):
            base += '/api'

        if not path.startswith('/'):
            path = '/' + path

        return base + path
    
    
    def _make_log_extra(self, res: requests.Response) -> dict:
        service = LoggingService(req=self.req)
        model = service.get(xan=LOG_TYPE_API, service_name=self.name)
        return {
            **model.model_dump(),
            'request': {
                API_LOGGING_URL_KEY: res.request.url,
                API_LOGGING_METHOD_KEY: res.request.method,
                API_LOGGING_HEADERS_KEY: res.request.headers,
                API_LOGGING_BODY_KEY: res.request.body
            },
            'response': {
                API_LOGGING_STATUS_KEY: res.status_code,
                API_LOGGING_HEADERS_KEY: res.headers,
                API_LOGGING_BODY_KEY: res.text
            }
        }


    def get(self, path: str):
        response = requests.get(self._build_url(path), headers=self.headers)
        if not response.ok:
            extra = self._make_log_extra(res=response)
            logger.info(path, extra=extra)
        return response


    def post(self, path: str, data: dict):
        url = self._build_url(path)
        if not url.endswith('/'):
            url += '/'
        response = requests.post(url, data=data, headers=self.headers)
        if not response.ok:
            extra = self._make_log_extra(res=response)
            logger.info(path, extra=extra)
        return response


    def put(self, path: str, data: dict):
        response = requests.put(self._build_url(path), data=data, headers=self.headers)
        if not response.ok:
            extra = self._make_log_extra(res=response)
            logger.info(path, extra=extra)
        return response


    def patch(self, path: str, data: dict):
        response = requests.patch(self._build_url(path), data=data, headers=self.headers)
        if not response.ok:
            extra = self._make_log_extra(res=response)
            logger.info(path, extra=extra)
        return response


    def delete(self, path: str):
        response = requests.delete(self._build_url(path), headers=self.headers)
        if not response.ok:
            extra = self._make_log_extra(res=response)
            logger.info(path, extra=extra)
        return response
