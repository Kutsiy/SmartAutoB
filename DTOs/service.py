from pydantic import BaseModel

class ServiceDto(BaseModel):
    name: str
    category: str
    text: str