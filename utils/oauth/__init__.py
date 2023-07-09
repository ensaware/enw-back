from abc import ABC, abstractmethod

from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from permission.v1.crud import get_permission

from authorization.v1.schema import TokenData
from utils.database import get_db
from utils.encryption import Encryption
from utils.exception import TypeMessage, Validate
from utils.exception.ensaware import EnsawareException
from utils.oauth.security import Security


class OAuth20(ABC):
    def __init__(self, url_callback: str) -> None:
        self.url_callback: str = url_callback
        self.encryption: Encryption = Encryption()

    @abstractmethod
    def authentication(self):
        pass


    @abstractmethod
    def get_data(self, request: Request):
        pass


    @abstractmethod
    def refresh_token(self, token: str):
        pass


class PermissionChecker:
    def __init__(self, code_name: str) -> None:
        self.__code_name: str = code_name

    def __call__(self, db: Session = Depends(get_db), token: TokenData = Depends(Security.get_token)) -> bool:
        query = get_permission(db, self.__code_name, token.profile)

        if query:
            return True
        else:
            raise EnsawareException(status.HTTP_401_UNAUTHORIZED, TypeMessage.VALIDATION.value, Validate.INVALID_AUTH.value)