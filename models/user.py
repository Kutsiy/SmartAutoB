from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from typing import List
from .role import Role
from .user_role import UserRole
from datetime import datetime

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    email: EmailStr = Field(index=True, unique=True)
    password: str
    phone_number: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    last_login: datetime | None = None
    roles: List[Role] = Relationship(back_populates='users', link_model=UserRole)
    isBanned: bool = False
    activeSymbols: str = Field(max_length=8)
    isActive: bool = False
    tokens: list["RefreshToken"] = Relationship(
    back_populates="user",
    sa_relationship_kwargs={"cascade": "all, delete-orphan"}
)
    appointments: list["Appointment"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})