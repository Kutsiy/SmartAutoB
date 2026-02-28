import jwt
from jwt.exceptions import InvalidTokenError
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from config import ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY
from DTOs.user import UserPayload

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(user_id: UUID, user_payload: UserPayload):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access",
        "id": str(user_payload.id),
        "email": user_payload.email,
        "password": user_payload.password
    }
    return jwt.encode(payload, ACCESS_TOKEN_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: UUID):
    jti = str(uuid4())
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "type": "refresh",
        "jti": jti,

    }
    return jwt.encode(payload, ACCESS_TOKEN_KEY, algorithm=ALGORITHM)