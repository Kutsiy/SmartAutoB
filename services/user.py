from enum import Enum
from tools import SessionDep
from DTOs import SignUpDto, LoginDto
from sqlmodel import select
from models import User
from fastapi import HTTPException

class Toggle(Enum):
    EXIST = 1
    NOT_EXIST = 2


def user_exist(toggle: Toggle, user_payload: LoginDto | SignUpDto,  session: SessionDep):
    user = session.exec(select(User).where(User.email == user_payload.email)).first()

    if toggle == Toggle.EXIST:
        if user:
            raise HTTPException(detail="User already exist")
    else:
        if not user:
            raise HTTPException(detail="User with this email not exist")
    
    return user


def create_user(user_payload: SignUpDto, hashed_password, session: SessionDep):
    user = User(name=user_payload.name, email=user_payload.email, password=hashed_password)
    session.add(user)
    session.commit(user)
    session.refresh(user)
    return user