from fastapi import APIRouter, Depends
from services import check_role
from models import Roles
from uuid import UUID
from tools import SessionDep
from DTOs import WorkTypeDto

work_type_router = APIRouter(prefix="/work/type")

@work_type_router.get("/all")
def get_all_work_types(session: SessionDep):
    pass

@work_type_router.get("")
def get_work_type_by_id(id: UUID, session: SessionDep):
    pass

@work_type_router.post("/create")
def create_work_type(type_payload: WorkTypeDto, check = Depends(check_role([Roles.ADMIN]))):
    pass

@work_type_router.patch("/update")
def update_work_type(id: UUID, session: SessionDep):
    pass

@work_type_router.delete("/delete")
def delete_work_type(id: UUID, check = Depends(check_role([Roles.ADMIN]))):
    pass