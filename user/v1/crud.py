from uuid import uuid4

from fastapi import status
from sqlalchemy.orm import Session

from utils.exception import TypeMessage, Validate
from utils.exception.ensaware import EnsawareException
from . import models, schema, ProfileType


def create_user(db: Session, user: schema.UserBase, user_read_model: bool = False) -> schema.User | schema.UserRead | None:
    user_dict = dict(user)

    if 'id' not in user_dict:
        user_dict['id'] = str(uuid4())

    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if user_read_model:
        return schema.UserRead.model_validate(db_user)
    else:
        return schema.User.model_validate(db_user)
    

def delete_user_id(db: Session, id: str, user_read_model: bool = False) -> schema.User | schema.UserRead | None:
    user = db.query(models.User).\
            filter(models.User.id == id, models.User.is_active)

    if not(user):
        return None
    
    user.update({
        models.User.modified: models.UTC,
        models.User.is_active: False
    }, synchronize_session=False)

    db.commit()

    user = db.query(models.User).\
            filter(models.User.id == id, models.User.is_active == False).\
            first()
    
    if user_read_model:
        return schema.UserRead.model_validate(user)
    else:
        return schema.User.model_validate(user)


def get_user_all(db: Session) -> list[schema.UserRead]:
    return db.query(models.User).\
            filter(models.User.is_active).\
            order_by(models.User.created.desc())


def get_user_id(db: Session, id: str, user_read_model: bool = False) -> schema.User | schema.UserRead | None:
    user = db.query(models.User).\
            filter(models.User.id == id, models.User.is_active).\
            first()

    if not(user):
        return None
    
    if user_read_model:
        return schema.UserRead.model_validate(user)
    else:
        return schema.User.model_validate(user)


def get_user_provider(db: Session, provider_id: str, user_read_model: bool = False) -> schema.User | schema.UserRead | None:
    user = db.query(models.User).\
            filter(
                models.User.provider_id == provider_id, 
                models.User.is_active
            ).\
            first()

    if not(user):
        return None
    
    if user_read_model:
        return schema.UserRead.model_validate(user)
    else:
        return schema.User.model_validate(user)


def get_profile(db: Session, profile: ProfileType) -> schema.Profile | None:
    profile = db.query(models.Profile).\
            filter(models.Profile.name == profile.value).\
            first()
    
    if profile:
        return schema.Profile.model_validate(profile)
    
    return None


def get_career_id(db: Session, id: str) -> schema.Career | None:
    career = db.query(models.Career).\
            filter(models.Career.id == id, models.Career.is_active).\
            first()
    
    if career:
        return schema.Career.model_validate(career)
    
    return None


def update_user_id(db: Session, id: str, update_user: schema.User, user_read_model: bool = False) -> schema.User | schema.UserRead | None:
    user_query = db.query(models.User).\
            filter(models.User.id == id, models.User.is_active)
    
    update_user.modified = models.UTC

    if not(user_query.first()):
        raise EnsawareException(status.HTTP_404_NOT_FOUND, TypeMessage.VALIDATION.value, Validate.INVALID_USER.value)
    
    user_query.update(update_user.model_dump(), synchronize_session=False)
    db.commit()

    if user_read_model:
        return schema.UserRead.model_validate(user_query.first())
    else:
        return schema.User.model_validate(user_query.first())