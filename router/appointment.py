from fastapi import APIRouter, Depends
from DTOs import AppointmentDto
from tools import SessionDep
from models import AppointmentStatus
from services import check_is_current_user_by_id, create_appointment_service, get_user_appointments_service, get_all_appointments_service, update_appointment_status_service
from uuid import UUID

appointment_router = APIRouter(prefix="/appointment")

@appointment_router.get('/all')
def get_all_appointments(session: SessionDep, search: str | None = None, status: AppointmentStatus | None = None, id: UUID | None = None):
    get_all_appointments_service(session=session, search=search, status=status, id=id)

@appointment_router.get('/user')
def get_user_appointments(id: UUID, session: SessionDep, check = Depends(check_is_current_user_by_id)):
    get_user_appointments_service(id=id, session=session)

@appointment_router.post('/create')
def create_appointment(appointment: AppointmentDto, session: SessionDep):
    create_appointment_service(appointment=appointment, session=session)

@appointment_router.patch('/update')
def update_appointment(id: UUID, status: AppointmentStatus, session: SessionDep):
    update_appointment_status_service(id=id, status=status, session=session)
