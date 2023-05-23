from uuid import uuid4

from sqlalchemy.orm import Session

from exception import TypeMessage, Validate
from exception.ensaware import EnsawareException
from . import models, schema, ProfileType


def create_user(db: Session, user: schema.UserBase) -> models.User:
    user_dict = dict(user)

    if 'id' not in user_dict:
        user_dict['id'] = str(uuid4())

    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return schema.User.from_orm(db_user)


def get_user_id(db: Session, id: str) -> models.User:
    return db.query(models.User).filter(models.User.id == id, models.User.is_active == True).first()


def get_user_provider(db: Session, provider_id: str) -> models.User:
    return db.query(models.User).filter(models.User.provider_id == provider_id, models.User.is_active == True).first()


def update_user_id(db: Session, id: str, update_user: schema.User):
    user_query = db.query(models.User).filter(models.User.id == id, models.User.is_active == True)

    user = user_query.first()

    if not(user):
        raise EnsawareException(404, TypeMessage.VALIDATION.value, Validate.INVALID_USER.value)
    
    user_query.update(update_user.dict(), synchronize_session='evaluate')
    db.commit()

    return user_query.first()


def get_profile(db: Session, profile: ProfileType) -> models.Profile:
    return db.query(models.Profile).filter(models.Profile.name == profile.value).first()