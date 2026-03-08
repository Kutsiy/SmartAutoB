from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from typing import List
from .role import Role
from .user_role import UserRole

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    email: EmailStr
    password: str
    roles: List[Role] = Relationship(back_populates='users', link_model=UserRole)
    isBanned: bool = False
    activeSymbols: str = Field(max_length=8)
    isActive: bool = False