from fastapi import APIRouter, Depends
from services import check_role, delete_user_by_id, find_all_users, find_user_by_id
from models import Roles
from uuid import UUID
from tools import SessionDep

user_router = APIRouter(prefix="/user", dependencies=[Depends(check_role([Roles.USER]))])

@user_router.get("/all")
def get_all_users(session: SessionDep):
    return find_all_users(session)

@user_router.get("")
def get_user(id: UUID, session: SessionDep):
    return find_user_by_id(id, session)

@user_router.delete("/delete")
def delete_user(id: UUID, session: SessionDep):
    delete_user_by_id(id, session)