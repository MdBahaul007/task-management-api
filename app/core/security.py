from pwdlib import PasswordHash
import jwt
from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"sub": subject, "exp": expire}

    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)  # OAuth2PasswordBearer It extracts the bearer token from the request's Authorization header.

def verify_access_token(token:str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            ALGORITHM
        )
        user_id = payload.get("sub")

        if not isinstance(user_id,str) or not user_id:
            raise InvalidTokenError("Invalid object")

        return payload
    except InvalidTokenError:
        raise
