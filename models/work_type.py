from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional
from .service import Service
from datetime import datetime

class WorkType(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    service_id: UUID = Field(foreign_key="service.id", ondelete="CASCADE")
    service: Optional["Service"] = Relationship(back_populates="work_types")
    name: str
    link_name: str
    text: str
    price: Decimal
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    is_deleted: bool = False

