from models import WorkType
from tools import SessionDep
from sqlmodel import select
from uuid import UUID
from DTOs import WorkTypeDto

def find_all_work_types(session: SessionDep):
    return session.exec(select(WorkType)).all()

def find_work_type_by_id(id: UUID, session: SessionDep):
    return session.exec(select(WorkType).where(WorkType.id == id)).first()

def update_work_type(id: UUID, work_type: WorkTypeDto, session: SessionDep):
    old_work_type = find_work_type_by_id(id, session)
    work_type_dump = work_type.model_dump(exclude=True)
    for key, value in work_type_dump.items():
        setattr(old_work_type, key, value)
    session.add(old_work_type)
    session.commit()
    session.refresh(old_work_type)
    return old_work_type


def create_work_type(work_type: WorkTypeDto, session: SessionDep):
    link_name = work_type.name.lower()
    work_type_payload = WorkType(name=work_type.name, link_name=link_name, text=work_type.text, price=work_type.price)
    session.add(work_type_payload)
    session.commit()
    session.refresh(work_type_payload)
    return work_type_payload

def delete_work_type(id: UUID, session: SessionDep):
    work_type = find_work_type_by_id(id, session)
    session.delete(work_type)
    session.commit()