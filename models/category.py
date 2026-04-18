from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

class Category(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    services: list["Service"] = Relationship(back_populates="category", sa_relationship_kwargs={"cascade": "all, delete-orphan"})