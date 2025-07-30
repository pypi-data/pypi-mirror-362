from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID


class ModuleModel(BaseModel):
    id: UUID
    name: str
    title: str
    version: str


class ProjectModel(BaseModel):
    id: UUID
    name: str
    caption: str
    description: str
    logo_url: str
    is_locked: bool
    tags: str


class ApplicationModel(BaseModel):
    id: UUID
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
    domain: str
    tags: str
    colour: str
    project: ProjectModel
    modules: Optional[List[ModuleModel]]
