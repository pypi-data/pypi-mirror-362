from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class AccountModel(BaseModel):
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
    client_id: str
    client_secret: str
    redirect_uri: str
    response_type: str
    grant_type: str
    domain: str
    scope: str
    aes_key: str
    rsa_public_pem: str
    rsa_private_pem: str
    rsa_passphrase: str
    algorithm: str
    claims: dict
    tags: str
    colour: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

