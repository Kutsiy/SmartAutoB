from sqlmodel import SQLModel
from uuid import UUID
from decimal import Decimal

class CategoryResponse(SQLModel):
    id: UUID
    name: str
    image_link: str
    services: list[ServiceResponse] = []

class WorkTypeService(SQLModel):
    id: UUID
    name: str

class WorkTypeResponse(SQLModel):
    id: UUID
    name: str
    link_name: str
    text: str
    price: Decimal
    duration: int
    service: WorkTypeService

class CategoryService(SQLModel):
    id: UUID
    name: str
    image_link: str

class ServiceResponse(SQLModel):
    id: UUID
    name: str
    text: str
    link_name: str
    category: CategoryService
    image_link: str
    work_types: list[WorkTypeResponse] = []
