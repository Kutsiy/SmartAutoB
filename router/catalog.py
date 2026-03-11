from fastapi import APIRouter, Depends
from services import check_role
from models import Roles
from uuid import UUID

catalog_router = APIRouter(prefix="/catalog")

@catalog_router.get("/all")
def get_all():
    pass

@catalog_router.post("/create")
def get_all(type_payload, check = Depends(check_role([Roles.ADMIN]))):
    pass

@catalog_router.delete("/create")
def get_all(id: UUID, check = Depends(check_role([Roles.ADMIN]))):
    pass