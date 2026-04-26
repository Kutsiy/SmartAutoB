from fastapi import APIRouter
from tools import SessionDep

statistic_router = APIRouter(prefix='/statistic')

@statistic_router.get('/user/cout')
def get_user_count(session: SessionDep):
    pass