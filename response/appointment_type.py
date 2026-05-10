from sqlmodel import SQLModel
from uuid import UUID
from decimal import Decimal
from datetime import date, time, datetime
from models import AppointmentStatus


class AppointmentUserResponse(SQLModel):
    id: UUID
    name: str
    email: str
    phoneNumber: str | None = None


class AppointmentWorkTypeResponse(SQLModel):
    id: UUID
    name: str
    price: Decimal
    duration: int


class AppointmentResponse(SQLModel):
    id: UUID
    user_id: UUID
    user: AppointmentUserResponse | None = None

    work_types: list[AppointmentWorkTypeResponse] = []

    cost: Decimal
    status: AppointmentStatus

    appointment_date: date
    appointment_time: time
    duration: int

    note: str | None = None
    cancel_reason: str | None = None
    done_note: str | None = None

    created_at: datetime
    canceled_at: datetime | None = None
    done_at: datetime | None = None
    startAt: datetime | None = None