from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from user.v1.schema import UserRead


class HistoricQRCodeBase(BaseModel):
    user_id: str

    class Config:
        orm_mode = True


class HistoricQrCode(HistoricQRCodeBase):
    id: str
    data: str | None
    is_active: bool
    created: datetime
    modified: datetime | None
    user: UserRead | None

    class Config:
        orm_mode = True


class UpdateHistoricQR(BaseModel):
    id: str
    data: str | None
    is_active: bool
    modified: datetime | None
    user_id: str

    class Config:
        orm_mode = True