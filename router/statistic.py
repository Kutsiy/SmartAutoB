from fastapi import APIRouter
from tools import SessionDep
from services import get_count_of_users

statistic_router = APIRouter(prefix='/statistic')

@statistic_router.get('/user/count')
def get_user_count(session: SessionDep):
    return get_count_of_users(session)

@statistic_router.get('/appointments')
def get_appointments_in_progress():
    pass