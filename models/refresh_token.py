from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4

class RefreshToken(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(default=None, foreign_key="user.id") 
    jti: str = Field(index=True, unique=True)
    expires_at: datetime
    revoked: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))