from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP
from sqlalchemy.orm import relationship

from utils.database import Base


UTC = datetime.now(timezone.utc)

class Library(Base):
    __tablename__ = 'library'

    id = Column(String(60), primary_key=True, index=True, default=str(uuid4()))
    title = Column(String(100))
    subtitle = Column(String(255), nullable=True)
    isbn_13 = Column(String(20))
    isbn_10 = Column(String(15), nullable=True)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    library_user = relationship('LibraryUser', back_populates='library')



class LibraryUser(Base):
    __tablename__ = 'library_user'

    id = Column(String(60), primary_key=True, index=True, default=str(uuid4()))
    library_id = Column(String(60), ForeignKey('library.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    created = Column(TIMESTAMP, default=UTC)
    modified = Column(TIMESTAMP, default=None)

    library = relationship('Library', back_populates='library_user')
    user = relationship('User', back_populates='library_user')