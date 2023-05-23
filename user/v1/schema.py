from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class CareerBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Career(CareerBase):
    id: str
    is_active: bool
    created: datetime
    modified: datetime | None

    class Config:
        orm_mode = True


class ProfileBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Profile(ProfileBase):
    id: str
    is_active: bool
    created: datetime
    modified: datetime | None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    provider_id: str
    provider: str
    display_name: str
    email: EmailStr
    picture: str | None
    profile_id: str
    refresh_token: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: str
    career_id: str | None
    is_active: bool
    created: datetime
    modified: datetime | None

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
    token_type: str = 'Bearer'
    refresh_token: str


class TokenData(BaseModel):
    email: EmailStr
    exp: int
    iat: int
    sub: str


class RefreshToken(BaseModel):
    refresh_token: str