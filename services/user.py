from enum import Enum
from tools import SessionDep, create_rundom_string, decode_access_token, decode_refresh_token
from DTOs import SignUpDto, LoginDto, UserPayload
from sqlmodel import select
from models import User, Roles
from fastapi import HTTPException, status, Depends
from .token import get_access_token, find_token_by_user_id_and_revoke, find_all_user_tokens_by_id_and_delete, get_refresh_token
from uuid import UUID


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

def update_user_name(nameUpdate, name, session: SessionDep):
    try:
        user = session.exec(select(User).where(User.name == name)).first()
        user.name = nameUpdate;
        session.add(user)
        session.commit()
        session.refresh(user)
    except:
        pass


def find_all_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return [UserPayload(id=user.id, name=user.name, email=user.email, role=[role.name for role in user.roles], isActivate=user.isActive) for user in users]

def find_user_by_id(user_id: UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(detail="User with this id not exist", status_code=status.HTTP_404_NOT_FOUND)
    return user

def find_user_by_id_r_payload(user_id: UUID, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(detail="User with this id not exist", status_code=status.HTTP_404_NOT_FOUND)
    return UserPayload(id=user.id, name=user.name, email=user.email, role=[role.name for role in user.roles], isActivate=user.isActive, isBanned=user.isBanned)

def find_user_by_email(email: str, session: SessionDep):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(detail="User with this email not exist", status_code=status.HTTP_404_NOT_FOUND)
    return user

    
def find_user_by_code_and_active(code:str, session: SessionDep):
    print(code)
    user = session.exec(select(User).where(User.activeSymbols == code)).first()
    if not user:
        raise HTTPException(detail="User with this code not exist", status_code=status.HTTP_404_NOT_FOUND)
    if user.isActive:
        raise HTTPException(detail="Account already active", status_code=status.HTTP_409_CONFLICT)
    user.isActive = True
    session.add(user)
    session.commit()


def check_user(session: SessionDep, token = Depends(get_access_token)):
    payload = decode_access_token(token)
    user = find_user_by_email(payload["email"], session)
    return user

def check_user_auth(user = Depends(check_user)):
    return user

def check_user_by_refresh_token(session: SessionDep, token = Depends(get_refresh_token)):
    payload = decode_refresh_token(token)
    user = find_user_by_id(payload["sub"], session)
    return user

def check_user_active(session: SessionDep, user: User = Depends(check_user)):
    if not user.isActive:
        raise HTTPException(detail="User account not activated", status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return user
    
def check_role(roles: list[Roles]):
    def check(user: User = Depends(check_user)):
        if not any(r.name in roles for r in user.roles):
            raise HTTPException(detail="You don`t have perrmision", status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return check

def check_user_banned(session: SessionDep, user: User = Depends(check_user)):
    if not user.isBanned:
        raise HTTPException(detail="You`re banned", status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return user

def change_isBanned_a_user(toggle: bool, user_id: UUID, session: SessionDep):
    user = find_user_by_id(user_id, session)
    user.isBanned = toggle
    find_all_user_tokens_by_id_and_delete(session)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def change_user_name(new_name: str, session: SessionDep, user: User = Depends(check_user)):
    user.name = new_name
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def check_is_current_user_by_id(id: str, user: User = Depends(check_user)):
    if id == user.id: return True
    else: raise HTTPException(status_code=403)

def delete_user_by_id(user_id: UUID, session: SessionDep):
    user = find_user_by_id(user_id, session)
    find_token_by_user_id_and_revoke(user_id, session)
    session.delete(user)
    session.commit()