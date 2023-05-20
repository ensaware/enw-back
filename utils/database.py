from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.settings import Settings


settings = Settings()


SQLALCHEMY_DATABASE_URL: str = f'{settings.database_api}://{settings.database_username}:{settings.database_pass}@{settings.database_host}:{settings.database_port}/{settings.database_name}'

ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()