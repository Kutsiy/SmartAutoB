from pydantic import BaseModel, Field, EmailStr
from models import Roles

class CreateAccountDto(BaseModel):
    name: str
    password: str = Field(max_length=10)
    email: EmailStr
    phone_number: str
    role: Roles