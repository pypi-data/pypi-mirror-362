
from pydantic import BaseModel


class UserAgentModel(BaseModel):
    is_mobile: bool
    is_tablet: bool
    is_touch_capable: bool
    is_pc: bool
    is_bot: bool
    is_email_client: bool
    browser_name: str
    browser_version: str
    os_name: str
    os_version: str
    device_name: str
    device_brand: str
    device_model: str
    
