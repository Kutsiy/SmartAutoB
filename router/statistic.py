from fastapi import APIRouter
from tools import SessionDep
from services import get_count_of_users, get_active_appointments, appointments_by_day_service, done_appointments_by_months_service, consultation_by_day_service, done_and_canceled_appointments_service

statistic_router = APIRouter(prefix='/statistic')

@statistic_router.get('/user/count')
def get_user_count(session: SessionDep):
    return get_count_of_users(session)

@statistic_router.get('/appointments/active')
def get_appointments_in_progress(session: SessionDep):
    return get_active_appointments(session=session)

@statistic_router.get('/appointments/months')
def get_done_appointments_by_months(session: SessionDep):
    return done_appointments_by_months_service(session=session)

@statistic_router.get('/appointments/day')
def get_appointments_by_day(sesssion: SessionDep):
    return appointments_by_day_service(session=sesssion)

@statistic_router.get('/consultation/day')
def get_consultation_by_day(session: SessionDep):
    return consultation_by_day_service(session=session)

@statistic_router.get('/appointments/completed-canceled')
def get_done_and_canceled_appointments(session: SessionDep):
    return done_and_canceled_appointments_service(session=session)