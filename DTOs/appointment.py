from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, time, date


class AppointmentDto(BaseModel):
    user_id: UUID
    note: str | None = None
    work_type_ids: list[UUID] = []
    appointment_time: time
    appointment_date: date

class AppointmentDateDto(BaseModel):
    appointment_date: date
