from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from nkunyim_util.models.user_model import UserModel


class TokenModel(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime


class SessionModel(BaseModel):
    token: Optional[TokenModel]
    user: Optional[UserModel]