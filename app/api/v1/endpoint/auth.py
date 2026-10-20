from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from app.models.user import User
from app.schemas.users import UserCreate, UserResponse, Login
from app.database import get_db
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    statement = select(User).where(User.email == user_data.email)
    existing_user = db.scalars(statement).one_or_none()

    if existing_user is not None:
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": f"User already exist with email id {user_data.email}",
            },
        )

    hashed_password = hash_password(user_data.password)

    new_user = User(email=user_data.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login_user(login_data: Login, db: Session = Depends(get_db)):
    statement = select(User).where(User.email == login_data.email)
    existing_user = db.scalars(statement).one_or_none()

    if existing_user is not None:
        is_valid_password = verify_password(
            login_data.password, existing_user.hashed_password
        )
        if is_valid_password == False:
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Invalid email or password",
                },
            )

        access_token = create_access_token(str(existing_user.id))

        return {
            "success": True,
            "message": "Login successful",
            "data": {"access_token": access_token, "token_type": "bearer"},
        }

    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": "User does not exist. Please register first",
        },
    )
