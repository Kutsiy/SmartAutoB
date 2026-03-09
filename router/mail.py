from fastapi import APIRouter
from services import find_user_by_code_and_active
from tools import SessionDep

mail_router = APIRouter(prefix="/mail")


@mail_router.get("/active")
async def check(code:str, session: SessionDep):
    find_user_by_code_and_active(code, session)