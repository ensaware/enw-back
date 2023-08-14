from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Boolean, Column, ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import relationship

from library.v1.models import LibraryUser
from permission.v1.models import PermissionProfile
from utils.database import Base


UTC = datetime.now(timezone.utc)


class Profile(Base):
    __tablename__ = 'profile'

    id = Column(String(60), primary_key=True, index=True, default=str(uuid4()))
    name = Column(String(100), index=True, unique=True)
    is_active = Column(Boolean, default=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    user = relationship('User', back_populates='profile')
    permission_profile = relationship('PermissionProfile', back_populates='profile')


class User(Base):
    __tablename__ = 'user'

    id = Column(String(60), primary_key=True, index=True, default=str(uuid4()))
    provider_id = Column(String(60), unique=True, index=True)
    provider = Column(String(50), nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    email = Column(String(100), index=True, unique=True)
    picture = Column(String(255), nullable=True)
    profile_id = Column(String(60), ForeignKey('profile.id'), nullable=False)
    career_id = Column(String(50), ForeignKey('career.id'), nullable=True)
    refresh_token = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    profile = relationship('Profile', back_populates='user')
    career = relationship('Career', back_populates='user')
    historic_qr_code = relationship('HistoricQrCode', back_populates='user')
    library_user = relationship('LibraryUser', back_populates='user')