from datetime import datetime, timedelta, timezone
from enum import Enum, unique
import logging

from authlib.jose import jwt
from fastapi import Depends, status
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPBearer
from typing import Annotated

from exception import Error, TypeMessage, Validate
from exception.ensaware import EnsawareException
from utils.settings import Settings
from .schema import User
from .schema import Token, TokenData


settings = Settings()
oauth2_token = HTTPBearer()


@unique
class ProfileType(Enum):
    STUDENT = 'estudiante'
    TEACHER = 'profesor'
    ADMINISTRATIVE = 'administrativo'
    ADMINISTRATOR = 'administrador'


class DecryptedToken:
    @staticmethod
    def get_token(token: Annotated[str, Depends(oauth2_token)]) -> TokenData:
        jwt = JWT()
        return jwt.decode(token.credentials)

class JWT:
    def __init__(self) -> None:
        self.__algorithm = 'HS512'
        self.__expire_minutes = settings.jwt_expire_minutes
        self.__encode = settings.encode
        self.__secret_key = settings.jwt_secret_key
        self.__utc = datetime.now(timezone.utc)


    def encode(self, user: User) -> Token:
        header = {
            'alg': self.__algorithm,
            'typ': 'JWT'
        }

        now: datetime = self.__utc.now()
        exp: datetime = now + timedelta(minutes=self.__expire_minutes)

        payload: dict = {
            'email': user.email,
            'exp': int(exp.timestamp()),
            'iat': int(now.timestamp()),
            'sub': user.id
        }

        try:
            token: str = jwt.encode(header, payload, self.__secret_key).decode(self.__encode)

            return Token(
                token = token,
                refresh_token = user.refresh_token
            )
        except Exception as ex:
            logging.exception(ex)
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR, Error.FAILED_CREATE_JWT)


    def decode(self, token: str) -> TokenData:
        try:
            payload: dict = jwt.decode(token, self.__secret_key)
            unix = int(self.__utc.now().timestamp())

            if unix > payload['exp']:
                raise EnsawareException(status.HTTP_401_UNAUTHORIZED, TypeMessage.ERROR.value, Error.EXPIRED_TOKEN.value)

            return TokenData(**payload)
        except EnsawareException as enw:
            logging.exception(enw)
            raise enw
        except Exception as ex:
            logging.exception(ex)
            raise EnsawareException(status.HTTP_401_UNAUTHORIZED, TypeMessage.VALIDATION.value, Validate.INVALID_JWT.value)