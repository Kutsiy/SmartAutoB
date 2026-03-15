from fastapi import APIRouter, Depends
from uuid import UUID


service_router = APIRouter(prefix="/service")

@service_router.get('/all')
def get_all_service():
    pass

@service_router.get('')
def get_service_by_id(id: UUID):
    pass

@service_router.post("/create")
def create_service():
    pass

@service_router.patch("/update")
def create_service(id: UUID):
    pass

@service_router.delete("delete")
def delete_service(id: UUID):
    pass