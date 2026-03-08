from fastapi import APIRouter
from services import find_user_by_code_and_active
from tools import SessionDep

mailRouter = APIRouter(prefix="/mail")


@mailRouter.get("/check")
async def check(code:str, session: SessionDep):
    find_user_by_code_and_active(code, session)