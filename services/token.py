from models import User, Role, RefreshToken
from tools import SessionDep, Tokens, create_tokens, REFRESH_TOKEN_EXPIRE_DAYS
from datetime import datetime, timezone, timedelta
from DTOs import UserPayload
from uuid import UUID
from sqlmodel import select
from fastapi import HTTPException, status, Request

def create_and_safe_token(user: User, role: list[Role], session: SessionDep):
    user_payload = UserPayload(email=user.email, name=user.name, role=[value.name for value in role])
    tokens: Tokens = create_tokens(user.id, user_payload=user_payload)
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = RefreshToken(user_id=user.id, jti=tokens.jti, expires_at=expires_at)
    session.add(refresh_token)
    session.commit()
    return tokens

def refresh_tokens(user: User, role: list[Role], session: SessionDep):
    old_refresh_token = session.exec(select(RefreshToken).where(RefreshToken.user_id == user.id, RefreshToken.revoked == False)).first()
    if not old_refresh_token or old_refresh_token.revoked:
        raise HTTPException(detail="Invalid refresh token", status_code=status.HTTP_406_NOT_ACCEPTABLE)
    old_refresh_token.revoked = True
    return create_and_safe_token(user, role, session)

def find_token_by_user_id_and_revoke(user_id: UUID, session: SessionDep):
    refresh_token = session.exec(select(RefreshToken).where(RefreshToken.user_id == user_id)).first()
    if not refresh_token:
        raise HTTPException(detail="Refresh token not found", status_code=status.HTTP_404_NOT_FOUND)
    refresh_token.revoked = True
    session.add(refresh_token)
    session.commit()

def get_access_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(detail="Access token not found", status_code=status.HTTP_401_UNAUTHORIZED)
        
    return token


def find_all_user_tokens_by_id(user_id: UUID,session: SessionDep):
    tokens: list[RefreshToken] = session.exec(select(RefreshToken).where(RefreshToken.user_id == user_id)).all()
    return tokens

def find_all_user_tokens_by_id_and_delete(user_id: UUID, session: SessionDep):
    tokens = find_all_user_tokens_by_id(user_id, session)
    for token in tokens:
        session.delete(token)
    session.commit()
