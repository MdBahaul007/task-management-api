from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=25)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool


class Login(BaseModel):
    email: EmailStr
    password: str
