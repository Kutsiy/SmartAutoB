from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from decimal import Decimal
from enum import Enum
from datetime import datetime

class AppointmentStatus(str, Enum):
    INPROCESSING = "INPROCESSING"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"



class AppointmentWorkTypeLink(SQLModel, table=True):
    appointment_id: UUID = Field(foreign_key="appointment.id", primary_key=True)
    work_type_id: UUID = Field(foreign_key="worktype.id", primary_key=True)
    price: Decimal


class Appointment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key='user.id', index=True, ondelete="CASCADE")
    user: "User" = Relationship(back_populates="appointments") 
    work_types: list["WorkType"] = Relationship(link_model=AppointmentWorkTypeLink)
    cost: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    status: AppointmentStatus = Field(
    default=AppointmentStatus.INPROCESSING,
    index=True
)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    appointment_time: datetime = Field(index=True)
    note: str | None = None
    cancel_reason: str | None = None
    finish_note: str | None = None
    updated_at: datetime | None = None
    canceled_at: datetime | None = None
    finished_at: datetime | None = None
