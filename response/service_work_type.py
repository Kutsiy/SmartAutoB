from sqlmodel import SQLModel
from uuid import UUID
from decimal import Decimal

class CategoryResponse(SQLModel):
    id: UUID
    name: str
    services: list[ServiceResponse] = []

class WorkTypeResponse(SQLModel):
    id: UUID
    name: str
    link_name: str
    text: str
    price: Decimal

class ServiceResponse(SQLModel):
    id: UUID
    name: str
    text: str
    work_types: list[WorkTypeResponse] = []
