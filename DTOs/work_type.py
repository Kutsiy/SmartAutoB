from pydantic import BaseModel

class WorkTypeDto(BaseModel):
    name: str
    link_name: str
    text: str
    price: Decimal