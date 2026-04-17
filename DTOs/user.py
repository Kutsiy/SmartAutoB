from pydantic import BaseModel, EmailStr
from uuid import UUID


class User(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    password: str

class UserPayload(BaseModel):
    email: EmailStr
    name: str
    role: list[str]
    isActivate: bool = False

class UserUpdateNamePayload(BaseModel):
    name: str