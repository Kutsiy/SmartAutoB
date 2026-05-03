from fastapi import APIRouter, Depends, UploadFile, File, Form
from uuid import UUID
from tools import SessionDep
from DTOs import ServiceDto
from services import find_all_services, find_service_by_id, create_service, update_service, delete_service_by_id, find_service_by_category_id, find_services_by_search_string
from response import ServiceResponse

service_router = APIRouter(prefix="/service")

@service_router.get('/all', response_model=list[ServiceResponse])
def get_all_service(session: SessionDep):
    return find_all_services(session)

@service_router.get('')
def get_service_by_id(id: UUID, session: SessionDep):
    return find_service_by_id(id, session)

@service_router.get('/category')
def get_service_by_id(id: UUID, session: SessionDep):
    return find_service_by_category_id(id, session)

@service_router.get('/search', response_model=list[ServiceResponse])
def get_services_by_search(session: SessionDep, category: str | None = None, search: str | None = None):
    return find_services_by_search_string(search=search, session=session, category=category)


@service_router.post("/create")
async def create(id: UUID, session: SessionDep, file: UploadFile = File(), name: str = Form(), text: str = Form()):
    service = ServiceDto(name=name, text=text)
    return await create_service(id=id, service=service, session=session, file=file)

@service_router.patch("/update", response_model=ServiceResponse)
async def update(id: UUID, session: SessionDep, file: UploadFile | None = File(default=None), name: str = Form(), text: str = Form()):
    service = ServiceDto(name=name, text=text)
    return await update_service(id, service, session, file=file)

@service_router.delete("/delete")
def delete(id: UUID, session: SessionDep):
    delete_service_by_id(id, session)