from datetime import datetime, timedelta, timezone
import logging

from authlib.jose import jwt
from fastapi import Depends, status
from fastapi.security import HTTPBearer
from typing import Annotated

from authorization.v1.schema import Token, TokenData
from utils.exception import Error, TypeMessage, Validate
from utils.exception.ensaware import EnsawareException
from utils.settings import Settings
from user.v1.schema import User


settings = Settings()
oauth2_token = HTTPBearer()


class Security:
    def __init__(self) -> None:
        self.__algorithm = 'HS512'
        self.__expire_minutes = settings.jwt_expire_minutes
        self.__encode = settings.encode
        self.__secret_key = settings.jwt_secret_key
        self.__utc = datetime.now(timezone.utc)


    def jwt_encode(self, user: User) -> Token:
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
            'profile': user.profile_id,
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


    def jwt_decode(self, token: str) -> TokenData:
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


    @staticmethod
    def get_token(token: Annotated[str, Depends(oauth2_token)]) -> TokenData:
        security = Security()
        return security.jwt_decode(token.credentials)