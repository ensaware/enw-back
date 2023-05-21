from datetime import datetime, timedelta, timezone
from enum import Enum, unique

from authlib.jose import jwt

from utils.settings import Settings
from .models import User
from .schema import Token, TokenData


settings = Settings()


@unique
class ProfileType(Enum):
    STUDENT = 'estudiante'
    TEACHER = 'profesor'
    ADMINISTRATIVE = 'administrativo'
    ADMINISTRATOR = 'administrador'


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

        token: str = jwt.encode(header, payload, self.__secret_key).decode(self.__encode)

        return Token(
            token = token,
            refresh_token = user.refresh_token
        )


    def decode(self, token: str) -> TokenData:
        payload: dict = jwt.decode(token, self.__secret_key)

        return TokenData(**payload)