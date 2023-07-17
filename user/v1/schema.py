from datetime import datetime
from pydantic import BaseModel, EmailStr


class CareerBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Career(CareerBase):
    id: str
    is_active: bool
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True


class ProfileBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Profile(ProfileBase):
    id: str
    is_active: bool
    created: datetime
    modified: datetime | None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    provider_id: str
    provider: str
    display_name: str
    email: EmailStr
    picture: str | None
    profile_id: str
    refresh_token: str

    class Config:
        from_attributes = True


class User(UserBase):
    id: str
    career_id: str | None
    is_active: bool
    created: datetime
    modified: datetime | None


    class Config:
        from_attributes = True


class UserRead(BaseModel):
    career: Career | None
    created: datetime
    display_name: str
    email: EmailStr
    id: str
    is_active: bool
    modified: datetime | None
    provider_id: str
    provider: str
    picture: str | None
    profile: Profile | None


    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    career_id: str | None