from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from decimal import Decimal

class AppointmentServiceLink(SQLModel, table=True):
    appointment_id: UUID = Field(foreign_key="appointment.id", primary_key=True)
    service_id: UUID = Field(foreign_key="service.id", primary_key=True)

class Appointment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key='user.id')
    services: list["Service"] = Relationship(link_model=AppointmentServiceLink)
    cost: Decimal
