from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class ProjectModel(BaseModel):
    id: UUID
    name: str
    title: str
    caption: str
    logo_url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    
class AppModel(BaseModel):
    id: UUID
    project: ProjectModel
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
    is_active: bool
    created_at: datetime
    updated_at: datetime
