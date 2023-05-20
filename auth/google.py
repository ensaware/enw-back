from time import sleep

from fastapi import Request
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests

from utils.settings import Settings

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
    

    def authentication(self) -> tuple[str, str]:
        flow = self.__get_config()
        
        return flow.authorization_url(
            access_type='offline',
            prompt='consent',
            include_granted_scopes='true',
        )
    

    def get_data(self, request: Request):
        flow = self.__get_config()

        flow.fetch_token(
            authorization_response=str(request.url),
        )

        credentials = flow.credentials
        
        sleep(1)

        idinfo = id_token.verify_token(credentials.id_token, requests.Request(), self.__settings.client_id_google)

        return flow.credentials, idinfo