from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Boolean, Column, String, TIMESTAMP
from sqlalchemy.orm import relationship

from user.v1.models import User
from utils.database import Base


UTC = datetime.now(timezone.utc)


class Career(Base):
    __tablename__ = 'career'

    id = Column(String(60), primary_key=True, index=True, default=str(uuid4()))
    name = Column(String(100), index=True, unique=True)
    is_active = Column(Boolean, default=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    user = relationship('User', back_populates='career')