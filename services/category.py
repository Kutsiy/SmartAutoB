from sqlmodel import SQLModel, select
from models import Category
from tools import SessionDep
from uuid import UUID
from DTOs import CategoryDto

def find_all_categories(session: SessionDep):
    return session.exec(select(Category)).all()

def find_category_by_id(id: UUID, session: SessionDep):
    return session.exec(select(Category).where(Category.id == id)).first()

def update_category_by_id(id: UUID, category: CategoryDto, session: SessionDep):
    old_category = find_category_by_id(id, session)
    category_dump = category.model_dump(exclude_unset=True)
    for key, value in category_dump.items():
        setattr(old_category, key, value)
    session.add(old_category)
    session.commit()
    session.refresh(old_category)
    return old_category

def create_category(category: CategoryDto, session: SessionDep):
    category_payload = Category(name=category.name)
    session.add(category_payload)
    session.commit()
    session.refresh(category_payload)
    return category_payload

def delete_category(id: UUID, session: SessionDep):
    category = find_category_by_id(id, session)
    session.delete(category)
    session.commit()