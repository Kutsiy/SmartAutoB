from sqlmodel import select
from models import Category
from tools import SessionDep
from tools.file import save_file
from uuid import UUID
from DTOs import CategoryDto
from fastapi import HTTPException, UploadFile
from datetime import datetime

def find_all_categories(session: SessionDep):
    return session.exec(select(Category)).all()

def check_category_by_name(name: str, session: SessionDep):
    existing = session.exec(
        select(Category).where(Category.name == name)
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Така категорія вже існує"
        )

def find_category_by_id(id: UUID, session: SessionDep):
    return session.exec(select(Category).where(Category.id == id)).first()

async def update_category_by_id(id: UUID, category: CategoryDto, file: UploadFile | None, session: SessionDep):
    file_name = ''
    if file: file_name = await save_file(file=file)
    old_category = find_category_by_id(id, session)
    old_category.name = category.name
    old_category.updated_at = datetime.utcnow()
    if file_name: old_category.image_link = file_name
    session.add(old_category)
    session.commit()
    session.refresh(old_category)
    return old_category

async def create_category(category: CategoryDto, session: SessionDep, file: UploadFile):
    check_category_by_name(name=category.name, session=session)
    file_name = await save_file(file=file, prefix='category')
    category_payload = Category(name=category.name, image_link=file_name)
    session.add(category_payload)
    session.commit()
    session.refresh(category_payload)
    return category_payload

def delete_category(id: UUID, session: SessionDep):
    category = find_category_by_id(id, session)
    session.delete(category)
    session.commit()

def search_category(search: str, session: SessionDep):
    return session.exec(select(Category).where(Category.name.contains(search))).all()