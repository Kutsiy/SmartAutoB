from fastapi import APIRouter
from uuid import UUID
from tools import SessionDep
from DTOs import CategoryDto
from services import find_all_categories, find_category_by_id, delete_category, create_category, update_category_by_id
from response import CategoryResponse

category_router = APIRouter(prefix='/category')

@category_router.get("/all", response_model=list[CategoryResponse])
def get_all_categories(session: SessionDep):
    return find_all_categories(session)

@category_router.get("")
def get_category_by_id(id: UUID, session: SessionDep):
    return find_category_by_id(id, session)

@category_router.patch("/update")
def update(id: UUID, category: CategoryDto, session: SessionDep):
    return update_category_by_id(id, category, session)

@category_router.post("/create")
def create(category: CategoryDto, session: SessionDep):
    return create_category(category, session)

@category_router.delete("/delete")
def delete(id: UUID, session: SessionDep):
    delete_category(id, session)