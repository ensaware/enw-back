import os

from fastapi import FastAPI

from exception.ensaware import EnsawareException, EnsawareExceptionHandler
from qr_code.v1.router import router as qr_code
from user.v1.router import router as user
from utils.settings import Settings


settings = Settings()
ensaware_exception_handler = EnsawareExceptionHandler()


app = FastAPI(
    title='Ensaware',
    version='0.0.1',
)

app.exception_handler(EnsawareException)(ensaware_exception_handler.ensaware)

if settings.debug == 1:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app.include_router(
    qr_code,
    prefix='/v1/qr-code',
    tags=['V1 - QR Code'],
)

app.include_router(
    user,
    prefix='/v1/user',
    tags=['V1 - User']
)