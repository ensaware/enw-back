from uuid import uuid4

from sqlalchemy.orm import Session
from . import models, schema


def create_qr_code(db: Session, qr_code: schema.QRCodeBase) -> models.QRCode:
    db_qr_code = models.QRCode(email=qr_code.email)
    db.add(db_qr_code)
    db.commit()
    db.refresh(db_qr_code)
    return db_qr_code


def get_qr_code(db: Session, id: str) -> models.QRCode:
    return db.query(models.QRCode).filter(models.QRCode.id == id).first()


def get_qr_code_email(db: Session, email: str) -> models.QRCode:
    return db.query(models.QRCode).filter(models.QRCode.email == email).first()


def create_historic_qr_code(db: Session, user_id: str) -> models.HistoricQrCode:
    db_historic = models.HistoricQrCode(user_id=user_id, id=str(uuid4()))
    db.add(db_historic)
    db.commit()
    db.refresh(db_historic)

    return db_historic


def get_historic_qr_code_id(db: Session, id: str) -> models.HistoricQrCode:
    return db.query(models.HistoricQrCode).\
        filter(models.HistoricQrCode.id == id, models.HistoricQrCode.is_active == True).\
        first()


def get_historic_qr_code_user_id(db: Session, user_id: str) -> list[schema.HistoricQrCode]:
    historic = db.query(models.HistoricQrCode)\
        .filter(models.HistoricQrCode.user_id == user_id)\
        .order_by(models.HistoricQrCode.created)

    return historic