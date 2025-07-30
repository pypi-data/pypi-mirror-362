from pydantic import BaseModel

class SmsModel(BaseModel):
    phone: str
    message: str
