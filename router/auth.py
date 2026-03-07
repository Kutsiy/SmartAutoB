from fastapi import APIRouter, Response
from sqlmodel import select
from DTOs import LoginDto, SignUpDto, UserPayload
from tools import get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, create_tokens, Tokens, verify_password
from uuid import UUID, uuid4
from tools import SessionDep
from models import User, RefreshToken
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

authRouter = APIRouter()

@authRouter.get("/login")
async def login(login: LoginDto, session: SessionDep):
    userCheck = session.exec(select(User).where(User.email == signUp.email)).first()

    if not userCheck:
        raise HTTPException(detail="User with this email not exist")
    
    verify = verify_password(login.password, userCheck.password)

    pass

@authRouter.get("/signup")
async def signUp(signUp: SignUpDto, session: SessionDep, response: Response)-> UserPayload:
    userCheck = session.exec(select(User).where(User.email == signUp.email)).first()

    if userCheck:
        raise HTTPException(detail="User already exist")

    hashed_password = get_password_hash(signUp.password)
    user = User(name=signUp.name, email=signUp.email, password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    user_payload = UserPayload(email=signUp.email, name=signUp.name)
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

