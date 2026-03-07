from sqlmodel import SQLModel, Field
from uuid import UUID

class UserRole(SQLModel, table=True):
    user_id: UUID = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: UUID = Field(default=None, foreign_key="role.id", primary_key=True)