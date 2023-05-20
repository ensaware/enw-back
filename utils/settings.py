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

    client_id_google = os.getenv('CLIENT_ID_GOOGLE')
    client_secret_google = os.getenv('CLIENT_SECRET_GOOGLE')

    debug = int(os.getenv('DEBUG')) or 0