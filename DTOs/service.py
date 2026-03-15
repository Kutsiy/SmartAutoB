from pydantic import BaseModel

class ServiceDto(BaseModel):
    name: str
    link_name: str
    category: str
    text: str