from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class AddressModel(BaseModel):
    id: UUID
    street_address: str
    postal_code: str
    locality: str
    city: str
    nation_id: UUID
    timezone: str
    language: str
    is_primary: bool
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class RoleModel(BaseModel):
    id: UUID
    name: str
    title: str
    is_admin: str
    
    
class UserModel(BaseModel):
    id: UUID
    username: str
    nickname: str
    first_name: str
    middle_name: str
    last_name: str
    email_address: str
    email_verified: bool
    email_verified_at: datetime
    phone_number: str
    phone_verified: bool
    phone_verified_at: datetime
    gender: str
    birth_date: datetime
    photo_url: str
    photo_verified: bool
    photo_verified_at: datetime
    profile: str
    is_pwd: bool
    is_active: bool
    is_admin: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    addreses: Optional[List[AddressModel]]
    role: Optional[RoleModel]
    permissions: Optional[List[str]]
