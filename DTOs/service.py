from pydantic import BaseModel

class ServiceDto(BaseModel):
    name: str
    text: str