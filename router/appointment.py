from fastapi import APIRouter, Depends
from DTOs import AppointmentDto
from tools import SessionDep
from models import AppointmentStatus
from services import check_is_current_user_by_id

appointment_router = APIRouter(prefix="/appointment")

@appointment_router.get('/all')
def create_appointment(session: SessionDep):
    pass

@appointment_router.get('/user')
def create_appointment(id: str, session: SessionDep, check = Depends(check_is_current_user_by_id)):
    pass

@appointment_router.post('/create')
def create_appointment(appointment: AppointmentDto):
    pass

@appointment_router.patch('/done')
def create_appointment(id: str, status: AppointmentStatus.DONE):
    pass

@appointment_router.patch('/cancel')
def create_appointment(id: str, status: AppointmentStatus.CANCELED):
    pass