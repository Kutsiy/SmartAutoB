from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime
from models import User

class ConsultationStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    IN_PROCESSING = "IN_PROCESSING"
    DONE = "DONE"
    CANCELED = "CANCELED"


class Consultation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    phone_number: str

    userId: UUID | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="consultations")

    status: ConsultationStatus = Field(
    default=ConsultationStatus.IN_PROCESSING,
    index=True
)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    note: str | None = None

    canceled_at: datetime | None = None
    done_at: datetime | None = None

