from uuid import uuid4

from fastapi import status
from sqlalchemy.orm import Session

from exception import TypeMessage, Validate
from exception.ensaware import EnsawareException
from . import models, schema, ProfileType


def create_user(db: Session, user: schema.UserBase) -> schema.User | None:
    user_dict = dict(user)

    if 'id' not in user_dict:
        user_dict['id'] = str(uuid4())

    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return schema.User.from_orm(db_user)


def get_user_id(db: Session, id: str) -> schema.User | None:
    user = db.query(models.User).\
            filter(models.User.id == id, models.User.is_active == True).\
            first()
    

    if user:
        return schema.User.from_orm(user)
    
    return None


def get_user_provider(db: Session, provider_id: str) -> schema.User | None:
    user = db.query(models.User).\
            filter(
                models.User.provider_id == provider_id, 
                models.User.is_active == True
            ).\
            first()

    if user:
        return schema.User.from_orm(user)
    
    return None


def update_user_id(db: Session, id: str, update_user: schema.User) -> schema.User | None:
    user_query = db.query(models.User).\
            filter(models.User.id == id, models.User.is_active == True)

    if not(user_query.first()):
        raise EnsawareException(status.HTTP_404_NOT_FOUND, TypeMessage.VALIDATION.value, Validate.INVALID_USER.value)
    
    user_query.update(update_user.dict(), synchronize_session='evaluate')
    db.commit()

    return schema.User.from_orm(user_query.first())


def get_profile(db: Session, profile: ProfileType) -> schema.Profile | None:
    profile = db.query(models.Profile).\
            filter(models.Profile.name == profile.value).\
            first()
    
    if profile:
        return schema.Profile.from_orm(profile)
    
    return None