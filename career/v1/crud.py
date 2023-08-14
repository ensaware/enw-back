from sqlalchemy.orm import Session

from . import models, schema


def get_career(db: Session) -> list[schema.Career] | None:    
    return db.query(models.Career).\
            filter(models.Career.is_active).\
            order_by(models.Career.name)


def get_career_id(db: Session, id: str) -> schema.Career | None:
    career = db.query(models.Career).\
            filter(models.Career.id == id, models.Career.is_active).\
            first()
    
    if career:
        return schema.Career.model_validate(career)
    
    return None