from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel

 
class ContinentModel(BaseModel):
    id: UUID
    code: str
    name: str


class CurrencyModel(BaseModel):
    id: UUID
    code: str
    name: str
    symbol: str
    decimals: int


class NationModel(BaseModel):
    id: UUID
    code: str
    name: str
    phone: str
    continent: ContinentModel
    currency: CurrencyModel
    capital: str
    languages: str
    north: Decimal
    south: Decimal
    east: Decimal
    west: Decimal
    flag: str
    flag_2x: str
    flag_3x: str
    flag_svg: str
    is_active: bool
