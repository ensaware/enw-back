from datetime import datetime
from pydantic import BaseModel


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