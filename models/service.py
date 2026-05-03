from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime

class Service(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    link_name: str
    image_link: str | None = None
    text: str
    category_id: UUID = Field(foreign_key='category.id', ondelete="CASCADE")
    category: Optional["Category"] = Relationship(back_populates="services")
    work_types: List["WorkType"] = Relationship(back_populates="service", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    is_deleted: bool = False
