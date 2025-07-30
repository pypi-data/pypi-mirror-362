from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID



class ItemModel(BaseModel):
    _id: UUID
    seq: int
    id: UUID
    name: str
    title: str
    caption: str
    icon: str
    path: str
    route: str
    tags: Optional[str]
    perms: Optional[List[str]]


class MenuModel(BaseModel):
    _id: UUID
    node: str
    seq: int
    id: UUID
    name: str
    title: str
    caption: str
    icon: str
    path: str
    route: str
    colour: str
    tags: Optional[str]
    items: Optional[List[ItemModel]]


class NavModel(BaseModel):
    node: str
    menus: List[MenuModel]
    
    
class AccessModel(BaseModel):
    navs: Optional[List[NavModel]]
    uix: dict