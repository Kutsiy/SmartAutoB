from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from enum import Enum
from typing import List
from .user_role import UserRole

class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class Role(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: Roles = Field(unique=True)
    users: List["User"] = Relationship(back_populates='roles', link_model=UserRole)