from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Boolean, Column, ForeignKey, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from utils.database import Base


UTC = datetime.now(timezone.utc)


class HistoricQrCode(Base):
    __tablename__ = 'historic_qr_code'
    
    id = Column(String(60), primary_key=True, index=True, default=str(uuid4()))
    user_id = Column(String(60), ForeignKey('user.id'), index=True)
    data = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    user = relationship('User', back_populates='historic_qr_code')