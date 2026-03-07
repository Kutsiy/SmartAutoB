from fastapi import APIRouter, Response
from sqlmodel import select
from DTOs import LoginDto, SignUpDto, UserPayload
from tools import get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, create_tokens, Tokens, verify_password
from uuid import UUID, uuid4
from tools import SessionDep
from models import User, RefreshToken, Role, UserRole
from datetime import datetime, timedelta, timezone
from services import user_exist, Toggle, create_user

authRouter = APIRouter()

@authRouter.get("/login")
async def login(login: LoginDto, session: SessionDep):
    user = user_exist(toggle=Toggle.NOT_EXIST, user_payload=login)
    
    verify = verify_password(login.password, user.password)

    pass

@authRouter.get("/signup")
async def signUp(signUp: SignUpDto, session: SessionDep, response: Response)-> UserPayload:
    user_exist(toggle=Toggle.EXIST, user_payload=signUp)

    hashed_password = get_password_hash(signUp.password)

    user = create_user(signUp, hashed_password=hashed_password)
    
    role: Role = session.exec(select(Role).where(Role.name == "USER")).first()

    userRole = UserRole(user_id=user.id, role_id=role.id)
    session.add(userRole)
    session.commit()

    user_payload = UserPayload(email=signUp.email, name=signUp.name, role=role.name)
    tokens: Tokens = create_tokens(user.id, user_payload=user_payload)
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = RefreshToken(user_id=user.id, jti=tokens.jti, expires_at=expires_at)
    session.add(refresh_token)
    session.commit()
    response.set_cookie("access_token", tokens.access_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60, httponly=True, secure=False, samesite="lax")    
    return user_payload

@authRouter.get("/logout")
async def logout():
    return (datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).date()

