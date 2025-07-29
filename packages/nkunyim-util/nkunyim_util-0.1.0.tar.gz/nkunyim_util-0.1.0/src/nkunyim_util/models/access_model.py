from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID


class RoleModel(BaseModel):
    id: UUID
    name: str
    title: str
    is_admin: str


class ItemModel(BaseModel):
    _id: UUID
    sequence: int
    id: UUID
    name: str
    title: str
    caption: str
    icon: str
    path: str
    route: str
    tags: Optional[str]


class MenuModel(BaseModel):
    _id: UUID
    node: str
    sequence: int
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
    role: Optional[RoleModel]
    navs: Optional[List[NavModel]]
    uix: dict