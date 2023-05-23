import logging

from fastapi import Request, status
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as api_requests
from sqlalchemy.orm import Session

from exception import Error, TypeMessage, Validate
from exception.ensaware import EnsawareException
from utils.settings import Settings
from user.v1 import JWT

from user.v1 import ProfileType
from user.v1.crud import create_user, get_profile, get_user_provider, update_user_id
from user.v1.schema import Profile, Token, User, UserBase

from . import Auth20


SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]


class GoogleProvider(Auth20):
    def __init__(self, url_callback: str) -> None:
        super().__init__(url_callback)

        self.__settings = Settings()
        self.__jwt = JWT()
        self.__baseUrl = 'https://oauth2.googleapis.com'


    def __get_config(self) -> Flow:
        flow =  Flow.from_client_config(
            client_config={
                'web': {
                    'client_id': self.__settings.client_id_google,
                    'client_secret': self.__settings.client_secret_google,
                    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                    'token_uri': f'{self.__baseUrl}/token',
                    'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob']
                }
            },
            scopes=SCOPES
        )

        flow.redirect_uri = self.url_callback

        return flow


    def __create_user(self, db: Session, token: dict, credentials) -> User:
        profile: Profile = get_profile(db, ProfileType.STUDENT)

        user_base = UserBase(
            provider_id = token.get('sub', None),
            provider = 'google',
            display_name = str(token.get('name', None)).title(),
            email = token.get('email', None),
            picture = token.get('picture', None),
            profile_id = profile.id,
            refresh_token = self.encryption.encrypt(credentials._refresh_token),
        )

        return create_user(db, user_base)
    

    def __get_token(self, db: Session, token: str) -> tuple[dict, User | None]:
        new_token = id_token.verify_token(
            id_token=token,
            request=requests.Request(),
            audience=self.__settings.client_id_google,
            clock_skew_in_seconds=10
        )

        provider_id: str = new_token.get('sub', None)

        user = get_user_provider(db, provider_id)

        if user:
            User.from_orm(user)

        return new_token, user
    

    def authentication(self) -> tuple[str, str]:
        flow = self.__get_config()
        
        return flow.authorization_url(
            access_type='offline',
            prompt='consent',
            include_granted_scopes='true',
        )
    

    def get_data(self, db: Session, request: Request) -> Token:
        flow = self.__get_config()
        flow.fetch_token(
            authorization_response=str(request.url),
        )

        credentials = flow.credentials

        token, get_user = self.__get_token(db, credentials.id_token)

        if not(get_user):
            get_user = self.__create_user(db, token, credentials)


        get_user.refresh_token = self.encryption.encrypt(credentials._refresh_token)
        get_user.picture = token.get('picture', None)
        get_user = User.from_orm(update_user_id(db, get_user.id, get_user))
        
        
        return self.__jwt.encode(get_user)
    

    def refresh_token(self, db: Session, token: str) -> Token:
        refresh_token = ''

        try:
            refresh_token = self.encryption.decrypt(token)
        except Exception as ex:
            logging.exception(ex)
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.VALIDATION.value, Validate.INVALID_REFRESH_TOKEN.value)

        body = {
            'client_id': self.__settings.client_id_google,
            'client_secret': self.__settings.client_secret_google,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        response = api_requests.post(
            f'{self.__baseUrl}/token',
            data=body
        )

        try:
            json_response = response.json()
            _, get_user = self.__get_token(db, json_response['id_token'])

            return self.__jwt.encode(get_user)
        except EnsawareException as enw:
            logging.exception(enw)
            raise enw
        except Exception as ex:
            logging.exception(ex)
            raise EnsawareException(status.HTTP_400_BAD_REQUEST, TypeMessage.ERROR.value, Error.REFRESH_TOKEN_FAILED.value)