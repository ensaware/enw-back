import os
from pydantic import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    database_host: str = os.getenv('DATABASE_HOST')
    database_username: str = os.getenv('DATABASE_USERNAME')
    database_pass: str = os.getenv('DATABASE_PASSWORD')
    database_port: str = os.getenv('DATABASE_PORT')
    database_name: str = os.getenv('DATABASE_NAME')
    database_api: str = 'mysql+mysqlconnector'

    fernet_pass = os.getenv('FERNET_PASS')
    encode: str = 'UTF-8'

    client_id_google: str = os.getenv('CLIENT_ID_GOOGLE')
    client_secret_google: str = os.getenv('CLIENT_SECRET_GOOGLE')

    debug: int = int(os.getenv('DEBUG')) or 0

    jwt_secret_key: str = os.getenv('JWT_SECRET_KEY')
    jwt_expire_minutes: int = int(os.getenv('JWT_EXPIRE_MINUTES'))

    cors_origins: str =  os.getenv('CORS_ORIGINS')
    cors_methods: str =  os.getenv('CORS_METHODS')

    callback_url_front: str = os.getenv('CALLBACK_URL_FRONT')