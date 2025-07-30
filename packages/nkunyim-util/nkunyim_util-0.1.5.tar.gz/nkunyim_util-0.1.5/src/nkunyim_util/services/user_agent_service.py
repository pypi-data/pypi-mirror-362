
from django.http import HttpRequest
from user_agents.parsers import UserAgent

from nkunyim_util.caches.user_agent_cache import UserAgentCache
from nkunyim_util.models.user_agent_model import UserAgentModel



class UserAgentService:
    
    def __init__(self, req: HttpRequest, session_key: str) -> None:
        self.cache = UserAgentCache(key=f"ua.{session_key}")
        self.session_key = session_key
        self.req = req
    
    def _make(self) -> UserAgentModel:
        ua_string = self.req.META.get('HTTP_USER_AGENT') or \
            self.req.headers.get('User-Agent') or \
            self.req.headers.get('user-agent', '')

        if isinstance(ua_string, bytes):
            ua_string = ua_string.decode('utf-8', 'ignore')

        ua = UserAgent(ua_string)

        data = {
            "is_mobile": ua.is_mobile,
            "is_tablet": ua.is_tablet,
            "is_touch_capable": ua.is_touch_capable,
            "is_pc": ua.is_pc,
            "is_bot": ua.is_bot,
            "is_email_client": ua.is_email_client,
            "browser_name": ua.browser.family,
            "browser_version": ua.browser.version_string,
            "os_name": ua.os.family,
            "os_version": ua.os.version_string,
            "device_name": ua.device.family,
            "device_brand": ua.device.brand,
            "device_model": ua.device.model,
        }
        
        user_agent = UserAgentModel(**data)
        self.cache.set(model=user_agent, timeout=60 * 60 * 24)
        
        return user_agent
    
    
    def get(self) -> UserAgentModel:
        return self.cache.get() or self._make()
