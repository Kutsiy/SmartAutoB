from enum import Enum
from tools import SessionDep, create_rundom_string, decode_access_token
from DTOs import SignUpDto, LoginDto
from sqlmodel import select
from models import User
from fastapi import HTTPException, status, Depends
from .token import get_access_token


class Toggle(Enum):
    EXIST = 1
    NOT_EXIST = 2


def user_exist(toggle: Toggle, user_payload: LoginDto | SignUpDto,  session: SessionDep):
    user = session.exec(select(User).where(User.email == user_payload.email)).first()

    if toggle == Toggle.EXIST:
        if user:
            raise HTTPException(detail="User already exist", status_code=status.HTTP_409_CONFLICT)
    else:
        if not user:
            raise HTTPException(detail="User with this email not exist", status_code=status.HTTP_404_NOT_FOUND)
    
    return user


def create_user(user_payload: SignUpDto, hashed_password, session: SessionDep):
    r_string: str = create_rundom_string()
    user = User(name=user_payload.name, email=user_payload.email, password=hashed_password, activeSymbols=r_string)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def find_user_by_email(email: str, session: SessionDep):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(detail="User with this email not exist", status_code=status.HTTP_404_NOT_FOUND)
    return user
    
def find_user_by_code_and_active(code:str, session: SessionDep):
    user = session.exec(select(User).where(User.activeSymbols == code)).first()
    if not user:
        raise HTTPException(detail="User with this code not exist", status_code=status.HTTP_404_NOT_FOUND)
    user.isActive = True
    session.add(user)
    session.commit()


def check_user_active(session: SessionDep, token = Depends(get_access_token)):
    payload = decode_access_token(token)
    user = find_user_by_email(payload["email"], session)
    if not user.isActive:
        raise HTTPException(detail="User account not activated", status_code=status.HTTP_406_NOT_ACCEPTABLE)
    