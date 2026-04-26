from fastapi import APIRouter, Depends
from services import check_role, delete_user_by_id, find_all_users, find_user_by_id_r_payload, check_user_auth, update_user_name
from models import Roles, User
from uuid import UUID
from tools import SessionDep
from DTOs import UserPayload, UserUpdateNamePayload

user_router = APIRouter(prefix="/user", dependencies=[Depends(check_role([Roles.USER]))])

@user_router.get("/all")
def get_all_users(session: SessionDep):
    return find_all_users(session)

@user_router.get("")
def get_user(id: UUID, session: SessionDep):
    return find_user_by_id_r_payload(id, session)

@user_router.get("/my")
def get_user( user: User = Depends(check_user_auth)):

    return UserPayload(id=user.id, name=user.name, email=user.email, role=[role.name for role in user.roles], isActivate=user.isActive)

@user_router.patch("/update")
def user_name_update(payload: UserUpdateNamePayload, session: SessionDep, check = Depends(check_user_auth)):
    update_user_name(nameUpdate=payload.name, name=check.name, session=session)

@user_router.delete("/delete")
def delete_user(id: UUID, session: SessionDep):
    delete_user_by_id(id, session)

@user_router.get('/isadmin')
def user_is_admin(check = Depends(check_role([Roles.ADMIN]))):
    return True
