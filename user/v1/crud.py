from sqlalchemy.orm import Session

from . import models, schema, ProfileType


def create_user(db: Session, user: schema.UserBase) -> models.User:
    db_user = models.User(**dict(user))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_id(db: Session, id: str) -> models.User:
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_provider(db: Session, provider_id: str) -> models.User:
    return db.query(models.User).filter(models.User.provider_id == provider_id).first()


def get_profile(db: Session, profile: ProfileType) -> models.Profile:
    return db.query(models.Profile).filter(models.Profile.name == profile.value).first()