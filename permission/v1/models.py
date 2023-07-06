from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import relationship

from utils.database import Base


UTC = datetime.now(timezone.utc)


class ContentType(Base):
    __tablename__ = 'content_type'

    id = Column(String(60), primary_key=True, index=True, default=str(uuid4()))
    model = Column(String(100), index=True, unique=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    permission = relationship('Permission', back_populates='content_type')


class Permission(Base):
    __tablename__ = 'permission'

    id = Column(String(60), primary_key=True, index=True, default=str(uuid4()))
    content_type_id = Column(String(60), ForeignKey('content_type.id'), nullable=False)
    code_name = Column(String(255), index=True, unique=True)
    description = Column(String(1000), nullable=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    content_type = relationship('ContentType', back_populates='permission')
    permission_profile = relationship('PermissionProfile', back_populates='permission')


class PermissionProfile(Base):
    __tablename__ = 'permission_profile'

    id = Column(String(60), primary_key=True, index=True, default=str(uuid4()))
    permission_id = Column(String(60), ForeignKey('permission.id'), nullable=False)
    profile_id = Column(String(60), ForeignKey('profile.id'), nullable=False)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    permission = relationship('Permission', back_populates='permission_profile')
    profile = relationship('Profile', back_populates='permission_profile')