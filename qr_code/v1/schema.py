from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class QRCodeBase(BaseModel):
    email: EmailStr = Field(
        ...,
    )


    class Config:
        orm_mode = True


class QRCode(QRCodeBase):
    id: str
    is_active: bool
    created: datetime
    modified: datetime | None

    class Config:
        orm_mode = True