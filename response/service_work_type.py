from sqlmodel import SQLModel
from uuid import UUID
from decimal import Decimal

class WorkTypeResponse(SQLModel):
    id: UUID
    name: str
    link_name: str
    text: str
    price: Decimal

class ServiceResponse(SQLModel):
    id: UUID
    name: str
    link_name: str
    category: str
    text: str
    work_types: list[WorkTypeResponse] = []