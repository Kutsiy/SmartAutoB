from pydantic import BaseModel
from uuid import UUID


class AppointmentDto(BaseModel):
    user_id: UUID
    note: str | None = None
    work_type_ids: list[UUID] = []