from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from app.core.security import oauth2_schema, verify_access_token
from sqlalchemy.orm import Session
from app.models.user import User
import jwt

from app.database import get_db


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
) -> User:

    try:
        payload = verify_access_token(token)
        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired password",
            headers={"WWW-Authenticate", "Bearer"},
        )

    statement = select(User).where(User.id == user_id)
    current_user = db.scalars(statement).one_or_none()

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
