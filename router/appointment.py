from fastapi import APIRouter

appointment_router = APIRouter(prefix="/appointment")

@appointment_router.post('/create')
def create_appointment():
    pass