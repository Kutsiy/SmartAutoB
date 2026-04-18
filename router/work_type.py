from fastapi import APIRouter, Depends
from services import check_role
from models import Roles
from uuid import UUID
from tools import SessionDep
from DTOs import WorkTypeDto
from services import find_all_work_types, find_work_type_by_id, add_work_type_to_service, update_work_type, delete_work_type

work_type_router = APIRouter(prefix="/work/type")

@work_type_router.get("/all")
def get_all_work_types(id: UUID, session: SessionDep):
    return find_all_work_types(id, session)

@work_type_router.get("")
def get_work_type_by_id(id: UUID, session: SessionDep):
    return find_work_type_by_id(id, session)

@work_type_router.post("/add")
def add_work_type(id: UUID, type_payload: WorkTypeDto, session: SessionDep):
    return add_work_type_to_service(id, type_payload, session)

@work_type_router.patch("/update")
def update_type(id: UUID, type_payload: WorkTypeDto, session: SessionDep, check = Depends(check_role([Roles.ADMIN]))):
    return update_work_type(id, type_payload, session)

@work_type_router.delete("/delete")
def delete_type(id: UUID, session: SessionDep, check = Depends(check_role([Roles.ADMIN]))):
    delete_work_type(id, session)