from uuid import uuid4

from sqlalchemy.orm import Session

from . import models, schema


def create_historic_qr_code(db: Session, user_id: str, update = False) -> schema.HistoricQrCode | schema.UpdateHistoricQR:
    query = models.HistoricQrCode(user_id=user_id, id=str(uuid4()))
    db.add(query)
    db.commit()
    db.refresh(query)

    if update:
        return schema.UpdateHistoricQR.model_validate(query)
    else:
        return schema.HistoricQrCode.model_validate(query)


def get_historic_qr_code_id(db: Session, id: str) -> schema.HistoricQrCode | None:
    query = db.query(models.HistoricQrCode).\
        filter(models.HistoricQrCode.id == id, models.HistoricQrCode.is_active == True).\
        first()
    
    return schema.HistoricQrCode.model_validate(query)


def get_historic_qr_code_user_id(db: Session, user_id: str) -> list[schema.HistoricQrCode] | None:
    query = db.query(models.HistoricQrCode)\
        .filter(models.HistoricQrCode.user_id == user_id)\
        .order_by(models.HistoricQrCode.created.desc())

    return query


def update_historic_qr_code_id(db: Session, id: str, update_history_qr_code: schema.UpdateHistoricQR) -> schema.HistoricQrCode | None:
    query = db.query(models.HistoricQrCode).\
            filter(models.HistoricQrCode.id == id, models.HistoricQrCode.is_active == True)
    
    update_history_qr_code.modified = models.UTC

    query.update(update_history_qr_code.model_dump(), synchronize_session='evaluate')
    db.commit()

    return schema.HistoricQrCode.model_validate(query.first())