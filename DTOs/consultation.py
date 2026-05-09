from pydantic import BaseModel, Field

class CreateConsultationDto(BaseModel):
    name: str 
    phone_number: str
    note: str = Field(max_length=300)