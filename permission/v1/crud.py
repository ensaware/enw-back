from sqlalchemy.orm import Session

from permission.v1 import models, schema

from authorization.v1.schema import TokenData
from utils.exception import TypeMessage, Validate
from utils.exception.ensaware import EnsawareException
from user.v1.schema import Profile


def get_permission(db: Session, code_name: str, profile_id: str) -> schema.ReadPermissionProfile | None:
    query = db.query(models.PermissionProfile).join(models.Permission).\
            filter(models.Permission.code_name == code_name, models.PermissionProfile.profile_id == profile_id).\
            first()
    
    if not(query):
        return None

    return schema.ReadPermissionProfile.from_orm(query)