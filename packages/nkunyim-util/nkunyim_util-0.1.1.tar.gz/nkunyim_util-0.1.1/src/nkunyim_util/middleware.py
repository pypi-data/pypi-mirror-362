import base64
import binascii
import json
from typing import Optional

from django.conf import settings
from django.http import HttpRequest

from nkunyim_util.encryption.rsa_encryption import RSAEncryption



class XanAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        self.process_request(request)
        return self.get_response(request)

    def _get_xan(self, request: HttpRequest) -> Optional[str]:
        header = request.META.get('HTTP_XAN_AUTHORIZATION')
        if not header:
            return None

        try:
            # Strip prefix/suffix or encoding markers
            cipher_token = header[2:-1]
            cipher_text = base64.b64decode(cipher_token)

            # Decrypt token
            plain_text = RSAEncryption().decrypt(cipher_text)
            service_name = json.loads(plain_text)


            if not bool(service_name and service_name == settings.NKUNYIM_SERVICE):
                return None

            return service_name
        except (ValueError, KeyError, json.JSONDecodeError, binascii.Error):
            return None


    def process_request(self, request: HttpRequest):
        service_name = self._get_xan(request)
        if service_name:
            request.service_name = service_name # type: ignore
        else:
            request.service_name = None # type: ignore



class MultipleProxyMiddleware:
    FORWARDED_FOR_FIELDS = [
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_FORWARDED_HOST",
        "HTTP_X_FORWARDED_SERVER",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if "," in request.META[field]:
                    parts = request.META[field].split(",")
                    request.META[field] = parts[-1].strip()
        return self.get_response(request)
    
    