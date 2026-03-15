from pydantic import BaseModel
from decimal import Decimal

class WorkTypeDto(BaseModel):
    name: str
    text: str
    price: Decimal