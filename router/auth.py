from typing import Annotated
from fastapi import APIRouter, Response, Request
from sqlmodel import select
from DTOs import LoginDto, SignUpDto, UserPayload
from tools import get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password, REFRESH_TOKEN_EXPIRE_DAYS, Tokens
from uuid import UUID, uuid4
from tools import SessionDep, decode_access_token
from fastapi import HTTPException, Depends
from models import User, Roles
from services import user_exist, Toggle, create_user, find_and_add_role, create_and_safe_token, find_token_by_user_id_and_revoke, find_user_by_email, send_email, EmailSchema, check_user_auth, refresh_tokens, check_user_by_refresh_token

auth_router = APIRouter(prefix="/auth")

def set_cookie(response: Response, tokens: Tokens):
    response.set_cookie("access_token", tokens.access_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60, httponly=True, secure=True, samesite="lax")
    response.set_cookie("refresh_token", tokens.refresh_token, REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24, httponly=True, secure=True, samesite="lax")


@auth_router.post("/login")
async def login(login: LoginDto, session: SessionDep, response: Response):
    user: User = user_exist(toggle=Toggle.NOT_EXIST, user_payload=login, session=session)
    
    if not verify_password(login.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    tokens = create_and_safe_token(user=user, role=user.roles, session=session)
    set_cookie(response, tokens)
    if not user.isActive:
        await send_email(email=EmailSchema(email=[user.email]), code=user.activeSymbols)
    return UserPayload(email=user.email, name=user.name, role=[value.name for value in user.roles], isActivate=user.isActive)

@auth_router.post("/signup")
async def signUp(signUp: SignUpDto, session: SessionDep, response: Response)-> UserPayload:
    user_exist(toggle=Toggle.EXIST, user_payload=signUp, session=session)

    hashed_password = get_password_hash(signUp.password)

    user: User = create_user(signUp, hashed_password=hashed_password, session=session)

    await send_email(email=EmailSchema(email=[user.email]), code=user.activeSymbols)
    
    role = find_and_add_role(user_id=user.id, session=session)

    tokens = create_and_safe_token(user, [role], session=session)
    set_cookie(response, tokens)    

    return UserPayload(email=user.email, name=user.name, role=[role.name], isActivate=user.isActive)

@auth_router.get("/logout")
def logout(response: Response, request: Request, session:SessionDep):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    token = request.headers.get("Authorization").split(" ")[1]
    decoded_token = decode_access_token(token)
    user = find_user_by_email(decoded_token["email"], session)
    find_token_by_user_id_and_revoke(user.id, session)

@auth_router.get("/refresh")
def refresh(response: Response, session: SessionDep, user: User = Depends(check_user_by_refresh_token)):
    tokens = refresh_tokens(user, user.roles, session)
    set_cookie(response, tokens)    
    return UserPayload(email=user.email, name=user.name, role=[value.name for value in user.roles], isActivate=user.isActive)

@auth_router.get("/check")
async def check(check = Depends(check_user_auth)):
    return True if check else False 