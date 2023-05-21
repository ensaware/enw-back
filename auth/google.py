from time import sleep

from fastapi import Request
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session

from utils.settings import Settings
from user.v1 import JWT

from user.v1 import ProfileType
from user.v1.crud import create_user, get_profile, get_user_provider
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


    def __get_config(self) -> Flow:
        flow =  Flow.from_client_config(
            client_config={
                'web': {
                    'client_id': self.__settings.client_id_google,
                    'client_secret': self.__settings.client_secret_google,
                    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                    'token_uri': 'https://oauth2.googleapis.com/token',
                    'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob']
                }
            },
            scopes=SCOPES
        )

        flow.redirect_uri = self.url_callback

        return flow


    def __create_user(self, db: Session, token: str, provider_id: str, credentials) -> User:
        profile: Profile = get_profile(db, ProfileType.STUDENT)

        user_base = UserBase(
            provider_id = provider_id,
            provider = 'google',
            display_name = str(token.get('name', None)).title(),
            email = token.get('email', None),
            picture = token.get('picture', None),
            profile_id = profile.id,
            refresh_token = self.encryption.encrypt(credentials._refresh_token),
        )

        return create_user(db, user_base)
    

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
        sleep(1)
        token = id_token.verify_token(credentials.id_token, requests.Request(), self.__settings.client_id_google)

        provider_id: str = token.get('sub', None)
        get_user: User = get_user_provider(db, provider_id)

        if not(get_user):
            get_user = self.__create_user(db, token, provider_id, credentials)
        
        
        return self.__jwt.encode(get_user)