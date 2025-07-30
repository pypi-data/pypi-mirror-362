
from typing import Optional
from pydantic import BaseModel

from nkunyim_util.models.location_model import LocationModel
from nkunyim_util.models.user_agent_model import UserAgentModel


class LoggingModel(BaseModel):
    xan: str
    service_name: str
    location: Optional[LocationModel]
    user_agent: Optional[UserAgentModel]