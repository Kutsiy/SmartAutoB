from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional
from .services import Services

class WorkTypes(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    service_id: UUID = Field(foreign_key="services.id")
    service: Optional[Services] = Relationship(back_populates="work_types")

    name: str
    text: str
    price: Decimal