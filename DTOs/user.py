from pydantic import BaseModel, EmailStr
from uuid import UUID

class User(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    password: str

class UserPayload(BaseModel):
    id: UUID
    email: EmailStr
    password: str