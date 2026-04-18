from pydantic import BaseModel

class CategoryDto(BaseModel):
    name: str