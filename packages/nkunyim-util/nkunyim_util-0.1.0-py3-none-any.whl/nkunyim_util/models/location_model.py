from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class LocationModel(BaseModel):
    user_ip: str
    accuracy_radius: int
    city: str
    continent_code: str
    continent_name: str 
    country_code: str 
    country_name: str 
    is_in_european_union: bool
    latitude: Decimal
    longitude: Decimal
    metro_code: Optional[str]
    postal_code: Optional[str] 
    region_code: str
    region_name: str
    time_zone: str
    dma_code: Optional[str] 
    region: Optional[str]
