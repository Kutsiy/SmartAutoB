from pydantic import BaseModel, EmailStr, Field

class SignUpDto(BaseModel):
    name: str
    password: str = Field(max_length=10)
    email: EmailStr