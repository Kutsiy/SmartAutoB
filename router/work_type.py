from fastapi import APIRouter, Depends
from services import check_role
from models import Roles
from uuid import UUID

work_type_router = APIRouter(prefix="/work/type")

@work_type_router.get("/all")
def get_all():
    pass

@work_type_router.post("/create")
def get_all(type_payload, check = Depends(check_role([Roles.ADMIN]))):
    pass

@work_type_router.delete("/create")
def get_all(id: UUID, check = Depends(check_role([Roles.ADMIN]))):
    pass