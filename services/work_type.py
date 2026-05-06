from models import WorkType, Service
from tools import SessionDep
from sqlmodel import select
from uuid import UUID
from DTOs import WorkTypeDto
from .service import find_service_by_id

def find_all_work_types(session: SessionDep, id: UUID | None = None):
    query = select(WorkType)

    if id:
        query = query.where(WorkType.service_id == id)

    return session.exec(query).all()

def find_work_type_by_id(id: UUID, session: SessionDep):
    return session.exec(select(WorkType).where(WorkType.id == id)).first()

def update_work_type(id: UUID, work_type: WorkTypeDto, session: SessionDep):
    old_work_type = find_work_type_by_id(id, session)
    old_work_type.name = work_type.name
    old_work_type.text = work_type.text
    old_work_type.duration = work_type.duration
    old_work_type.price = work_type.price
    session.add(old_work_type)
    session.commit()
    session.refresh(old_work_type)
    return old_work_type


def add_work_type_to_service(id: UUID, work_type: WorkTypeDto, session: SessionDep):
    service = find_service_by_id(id, session)
    link_name = work_type.name.lower().strip().replace(" ", "/")
    work_type_payload = WorkType(name=work_type.name, link_name=link_name, text=work_type.text, price=work_type.price, service=service, duration=work_type.duration)
    session.add(work_type_payload)
    session.commit()
    session.refresh(work_type_payload)
    return work_type_payload

def delete_work_type(id: UUID, session: SessionDep):
    work_type = find_work_type_by_id(id, session)
    session.delete(work_type)
    session.commit()

def work_type_search(session: SessionDep, search: str | None = None, service: str | None = None):
    query = select(WorkType)

    if search:
        query = query.where(WorkType.name.ilike(f"%{search}%"))

    if service:
        query = query.join(WorkType.service).where(Service.name == service)

    return session.exec(query).all()