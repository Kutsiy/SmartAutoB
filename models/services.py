from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import List

class Services(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    link_name: str
    category: str
    text: str

    work_types: List["WorkTypes"] = Relationship(back_populates="service", sa_relationship_kwargs={"cascade": "all, delete-orphan"})