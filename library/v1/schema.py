from datetime import datetime
from pydantic import BaseModel

from user.v1.schema import UserRead


class LibraryBase(BaseModel):
    title: str
    subtitle: str | None
    isbn_13: str
    isbn_10: str | None


    class Config:
        from_attributes = True


class Library(LibraryBase):
    id: str
    created: datetime
    modified: datetime | None


    class Config:
        from_attributes = True


class LibraryUserBase(BaseModel):
    library_id: str
    user_id: str


    class Config:
        from_attributes = True


class LibraryUser(BaseModel):
    id: str
    library: Library
    user: UserRead
    created: datetime
    modified: datetime | None


    class Config:
        from_attributes = True