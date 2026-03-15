from pydantic import BaseModel
from decimal import Decimal

class WorkTypeDto(BaseModel):
    name: str
    link_name: str
    text: str
    price: Decimal