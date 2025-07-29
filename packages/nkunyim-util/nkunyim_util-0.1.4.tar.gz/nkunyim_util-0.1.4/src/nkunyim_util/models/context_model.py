from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel

from .app_model import AccountModel
from .location_model import LocationModel
from .nation_model import NationModel
from .access_model import NavModel
from .page_model import PageModel
from .user_model import UserModel


class ContextModel(BaseModel):
    id: UUID
    account: AccountModel
    mode: str
    name: str
    title: str
    caption: str
    description: str
    keywords: str
    image_url: str
    logo_url: str
    logo_light_url: str
    logo_dark_url: str
    icon_url: str
    icon_light_url: str
    icon_dark_url: str
    tags: str
    colour: str
    is_active: bool
    location: LocationModel
    nation: NationModel
    user: Optional[UserModel]
    page: PageModel
    uix: dict
    navs: Union[list[NavModel], None]
    root: str
    
    