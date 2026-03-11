from fastapi import APIRouter, Depends
from uuid import UUID


service_router = APIRouter(prefix="/service")

@service_router.get('')
def get_service_by_id(id: UUID):
    pass