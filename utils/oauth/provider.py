from enum import Enum, unique

from fastapi import status
from sqlalchemy.orm import Session

from utils.exception import TypeMessage, Validate
from utils.exception.ensaware import EnsawareException
from .google import GoogleProvider


@unique
class Provider(Enum):
    GOOGLE = 'google'


class SelectProvider:
    @staticmethod
    def select(provider: Provider, url_callback: str, db: Session):
        if provider == Provider.GOOGLE:
            return GoogleProvider(url_callback, db)
        else:
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Validate.INVALID_PROVIDER.value)