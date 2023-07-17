from datetime import datetime
from pydantic import BaseModel

from user.v1.schema import Profile


class ContentTypeBase(BaseModel):
    model: str

    class Config:
        from_attributes = True


class ContentType(ContentTypeBase):
    id: str
    created: datetime
    modified: datetime | None


    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    content_type_id: str
    code_name: str
    description: str


    class Config:
        from_attributes = True


class Permission(PermissionBase):
    id: str
    created: datetime
    modified: datetime | None


    class Config:
        from_attributes = True


class PermissionProfileBase(BaseModel):
    permission_id: str
    profile_id: str


    class Config:
        from_attributes = True


class PermissionProfile(PermissionProfileBase):
    id: str
    created: datetime
    modified: datetime | None


    class Config:
        from_attributes = True


class ReadPermissionProfile(BaseModel):
    id: str
    permission: Permission
    profile: Profile
    created: datetime
    modified: datetime | None


    class Config:
        from_attributes = True