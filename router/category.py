from fastapi import APIRouter, UploadFile, File, Form
from uuid import UUID
from tools import SessionDep
from DTOs import CategoryDto
from services import find_all_categories, find_category_by_id, delete_category, create_category, update_category_by_id, search_category
from response import CategoryResponse

category_router = APIRouter(prefix='/category')

@category_router.get("/all", response_model=list[CategoryResponse])
def get_all_categories(session: SessionDep):
    return find_all_categories(session)

@category_router.get("")
def get_category_by_id(id: UUID, session: SessionDep):
    return find_category_by_id(id, session)


@category_router.get("/search")
def find_category_by_search_string(search: str, session: SessionDep):
    return search_category(search=search, session=session)

@category_router.patch("/update")
async def update(id: UUID, session: SessionDep, file: UploadFile | None = File(default=None), name: str = Form()):
    category = CategoryDto(name=name)
    print(id)
    return await update_category_by_id(id=id, category=category, file=file, session=session)

@category_router.post("/create")
async def create(session: SessionDep, file: UploadFile = File(), name: str = Form()):
    print(file)
    category = CategoryDto(name=name)
    return await create_category(category=category, file=file, session=session)

@category_router.delete("/delete")
def delete(id: UUID, session: SessionDep):
    delete_category(id, session)