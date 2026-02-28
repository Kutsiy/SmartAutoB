from pydantic import BaseModel, EmailStr

class SignUpDto(BaseModel):
    name: str
    password: str
    email: EmailStr