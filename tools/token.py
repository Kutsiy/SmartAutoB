import jwt
from jwt.exceptions import InvalidTokenError
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from config import ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY
from DTOs.user import UserPayload

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 14

class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    jti: str

def create_access_token(user_id: UUID, user_payload: UserPayload):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": int(expire.timestamp()),
        "type": "access",
        "email": user_payload.email,
        "name": user_payload.name
    }
    return jwt.encode(payload, ACCESS_TOKEN_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: UUID, jti: str):
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(user_id),
        "exp": int(expire.timestamp()),
        "type": "refresh",
        "jti": jti,

    }
    return jwt.encode(payload, REFRESH_TOKEN_KEY, algorithm=ALGORITHM)

def create_tokens(user_id: UUID, user_payload: UserPayload)-> Tokens:
    jti = str(uuid4())
    access_token = create_access_token(user_id, user_payload)
    refresh_token = create_refresh_token(user_id, jti)
    return Tokens(
        access_token=access_token,
        refresh_token=refresh_token,
        jti=jti
    )