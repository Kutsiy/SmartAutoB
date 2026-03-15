from tools import SessionDep
from models import Service
from sqlmodel import select
from uuid import UUID
from DTOs import ServiceDto

def find_all_services(session: SessionDep):
    services = session.exec(select(Service)).all()
    return services

def find_service_by_id(id: UUID, session: SessionDep):
    service = session.exec(select(Service).where(Service.id == id)).first()
    return service

def create_service(service: ServiceDto, session: SessionDep):
    link_name = service.name.lower()
    service_payload = Service(name=service.name, link_name=link_name, category=service.category, text=service.text)
    session.add(service_payload)
    session.commit()
    session.refresh(service_payload)
    return service_payload

def update_service(id: UUID, service: ServiceDto, session: SessionDep):
    old_service = find_service_by_id(id, session)
    update_data = service.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(old_service, key, value)
    session.add(old_service)
    session.commit()
    session.refresh(old_service)
    return old_service

def delete_service_by_id(id: UUID, session: SessionDep):
    service = find_service_by_id(id, session)
    session.delete(service)
    session.commit()