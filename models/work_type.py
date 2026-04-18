from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional
from .service import Service

class WorkType(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    service_id: UUID = Field(foreign_key="service.id", ondelete="CASCADE")
    service: Optional["Service"] = Relationship(back_populates="work_types")

    name: str
    link_name: str
    text: str
    price: Decimal

