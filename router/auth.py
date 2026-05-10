from fastapi import APIRouter, Response, Request
from sqlmodel import select
from DTOs import LoginDto, SignUpDto, UserPayload, CreateAccountDto
from tools import get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password, REFRESH_TOKEN_EXPIRE_DAYS, Tokens
from uuid import UUID, uuid4
from tools import SessionDep, decode_access_token
from fastapi import HTTPException, Depends
from models import User, Roles
from services import user_exist, Toggle, create_user, find_and_add_role, create_and_save_token, find_token_by_user_id_and_revoke, find_user_by_email, send_email, EmailSchema, check_user_auth, refresh_tokens, check_user_by_refresh_token, get_access_token

def set_cookie(response: Response, tokens: Tokens):
    response.set_cookie("access_token", tokens.access_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60, httponly=True, secure=True, samesite="lax")
    response.set_cookie("refresh_token", tokens.refresh_token, REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24, httponly=True, secure=True, samesite="lax")

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login")
async def login(login: LoginDto, session: SessionDep, response: Response):
    user: User = user_exist(toggle=Toggle.NOT_EXIST, user_payload=login, session=session)
    
    if not verify_password(login.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    tokens = create_and_save_token(user=user, role=user.roles, session=session)

    set_cookie(response, tokens)
    if not user.isActive:
        await send_email(email=EmailSchema(email=[user.email]), code=user.activeSymbols)
    return UserPayload(id=user.id, email=user.email, name=user.name, role=[value.name for value in user.roles], isActivate=user.isActive)

@auth_router.post("/signup")
async def signUp(sign_up: SignUpDto, session: SessionDep, response: Response)-> UserPayload:
    user_exist(toggle=Toggle.EXIST, user_payload=sign_up, session=session)

    hashed_password = get_password_hash(sign_up.password)

    user: User = create_user(sign_up, hashed_password=hashed_password, session=session)

    await send_email(email=EmailSchema(email=[user.email]), code=user.activeSymbols)
    
    role = find_and_add_role(user_id=user.id, session=session)

    tokens = create_and_save_token(user, [role], session=session)

    set_cookie(response, tokens)    

    return UserPayload(id=user.id, email=user.email, name=user.name, role=[role.name], isActivate=user.isActive)

@auth_router.post('/create')
def create_account(create_account: CreateAccountDto, session: SessionDep):
    user_exist(toggle=Toggle.EXIST, user_payload=create_account, session=session)

    hashed_password = get_password_hash(create_account.password)

    user: User = create_user(create_account, hashed_password=hashed_password, session=session, user_is_active=True)

    role = find_and_add_role(user_id=user.id, session=session, default_role=create_account.role)
    create_and_save_token(user, [role], session=session)

    return UserPayload(id=user.id, email=user.email, name=user.name, role=[value.name for value in user.roles], isActivate=user.isActive)


@auth_router.get("/logout")
def logout(response: Response, request: Request, session:SessionDep):
    token = get_access_token(request=request)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    decoded_token = decode_access_token(token)
    user = find_user_by_email(decoded_token["email"], session)
    find_token_by_user_id_and_revoke(user.id, session)

@auth_router.get("/refresh")
def refresh(response: Response, session: SessionDep, user: User = Depends(check_user_by_refresh_token)):
    tokens = refresh_tokens(user, user.roles, session)
    set_cookie(response, tokens)    
    return UserPayload(id=user.id, email=user.email, name=user.name, role=[value.name for value in user.roles], isActivate=user.isActive)

@auth_router.get("/check")
async def check(check = Depends(check_user_auth)):
    return True if check else False 
