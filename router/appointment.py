from fastapi import APIRouter, Depends
from DTOs import AppointmentDto, AppointmentDateDto
from tools import SessionDep
from models import AppointmentStatus, Appointment
from services import check_is_current_user_by_id, create_appointment_service, get_user_appointments_service, get_all_appointments_service, update_appointment_status_service, get_date_for_appointment_service
from uuid import UUID
from response import AppointmentResponse

appointment_router = APIRouter(prefix="/appointment")

@appointment_router.get('/all', response_model=list[AppointmentResponse])
def get_all_appointments(session: SessionDep, search: str | None = None, status: AppointmentStatus | None = None, id: UUID | None = None):
    return get_all_appointments_service(session=session, search=search, status=status, id=id)

@appointment_router.get('/user', response_model=list[AppointmentResponse])
def get_user_appointments(id: UUID, session: SessionDep):
    return get_user_appointments_service(id=id, session=session)

@appointment_router.post('/date')
def get_date_for_appointment(session: SessionDep, appointment_date: AppointmentDateDto):
    return get_date_for_appointment_service(session=session, appointment_date=appointment_date)

@appointment_router.post('/create')
def create_appointment(appointment: AppointmentDto, session: SessionDep):
    create_appointment_service(appointment=appointment, session=session)

@appointment_router.patch('/update')
def update_appointment(id: UUID, status: AppointmentStatus, session: SessionDep):
    update_appointment_status_service(id=id, status=status, session=session)
