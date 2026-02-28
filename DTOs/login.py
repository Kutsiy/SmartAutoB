from pydantic import BaseModel, EmailStr

class LoginDto(BaseModel):
    password: str
    email: EmailStr