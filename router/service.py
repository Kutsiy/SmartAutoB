from fastapi import APIRouter, Depends
from uuid import UUID
from tools import SessionDep
from DTOs import ServiceDto
from services import find_all_services, find_service_by_id, create_service, update_service, delete_service_by_id
from response import ServiceResponse

service_router = APIRouter(prefix="/service")

@service_router.get('/all', response_model=list[ServiceResponse])
def get_all_service(session: SessionDep):
    return find_all_services(session)

@service_router.get('')
def get_service_by_id(id: UUID, session: SessionDep):
    return find_service_by_id(id, session)

@service_router.post("/create")
def create(service: ServiceDto, session: SessionDep):
    return create_service(service, session)

@service_router.patch("/update")
def update(id: UUID, service: ServiceDto, session: SessionDep):
    return update_service(id, service, session)

@service_router.delete("/delete")
def delete(id: UUID, session: SessionDep):
    delete_service_by_id(id, session)