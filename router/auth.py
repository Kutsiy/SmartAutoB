from fastapi import APIRouter
from DTOs import LoginDto, SignUpDto
from tools import get_password_hash, create_refresh_token, create_access_token
from uuid import UUID, uuid4


authRouter = APIRouter()

@authRouter.get("/login")
async def login(login: LoginDto):
    print(create_access_token(uuid4()))
    pass

@authRouter.get("/signup")
async def signUp(signUp: SignUpDto):
    hashed_password = get_password_hash(signUp.password)
    pass

@authRouter.get("/logout")
async def logout():
    pass

