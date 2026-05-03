from tools import SessionDep
from tools.file import save_file
from models import Service, Category
from sqlmodel import select
from uuid import UUID
from DTOs import ServiceDto
from sqlalchemy.orm import selectinload
from .category import find_category_by_id
from fastapi import UploadFile, HTTPException, status


def check_service_by_name(name: str, session: SessionDep):
    check = session.exec(select(Service).where(Service.name == name)).first()
    if(check):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такий сервіс вже існує")

def find_all_services(session: SessionDep):
    services = session.exec(select(Service).options(selectinload(Service.work_types))).all()
    for s in services:
        print(s.work_types)
    return services

def find_service_by_id(id: UUID, session: SessionDep):
    service = session.exec(select(Service).where(Service.id == id)).first()
    return service

def find_service_by_category_id(id: UUID, session: SessionDep):
    service = session.exec(select(Service).where(Service.category_id == id)).all()
    return service

async def create_service(id: UUID, service: ServiceDto, session: SessionDep, file: UploadFile):
    check_service_by_name(name=service.name, session=session)
    category = find_category_by_id(id, session)
    link_name = service.name.lower().strip().replace(" ", "/")
    file_link = await save_file(file=file, prefix='service')
    service_payload = Service(name=service.name, link_name=link_name, category=category, text=service.text, image_link=file_link)
    session.add(service_payload)
    session.commit()
    session.refresh(service_payload)
    return service_payload

async def update_service(id: UUID, service: ServiceDto, session: SessionDep, file: UploadFile | None):
    file_name = ''
    if file: file_name = await save_file(file=file)
    old_service = find_service_by_id(id, session)
    old_service.name = service.name
    old_service.text = service.text
    if file_name: old_service.image_link = file_name
    session.add(old_service)
    session.commit()
    session.refresh(old_service)
    return old_service

def delete_service_by_id(id: UUID, session: SessionDep):
    service = find_service_by_id(id, session)
    session.delete(service)
    session.commit()

def find_services_by_search_string(session: SessionDep, category: str | None = None, search: str | None = None):
    query = select(Service)

    if search:
        query = query.where(Service.name.ilike(f"%{search}%"))

    if category:
        query = query.join(Service.category).where(Category.name == category)

    print(category)
    return session.exec(query).all()