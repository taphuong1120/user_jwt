from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from typing import Optional,Union

class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    role: int = 0
    disabled: bool = False

class UpdateUserSchema(BaseModel):
    # password: constr(min_length=8)
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    photo: Optional[str] = None
    bio: Optional[str] = None
    dnft: Optional[int] = None
    dp: Optional[int] = None

    class Config:
        orm_mode = True
    

class LoginUserSchema(BaseModel):
    username: str
    password: constr(min_length=8)


class UserResponse(UserBaseSchema):
    id: int
    twitter: Optional[str]
    telegram: Optional[str]
    photo: Optional[str]
    bio: Optional[str]
    wallet: Optional[str]
    dnft: Optional[int] = 0
    dp: Optional[int] = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True