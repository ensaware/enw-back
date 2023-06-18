import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from exception.ensaware import EnsawareException, EnsawareExceptionHandler
from qr_code.v1.router import router as qr_code
from user.v1.router import router as user
from utils.settings import Settings


# Se deja habilitado hasta tener un dominio con el protocolo https
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


settings = Settings()
ensaware_exception_handler = EnsawareExceptionHandler()


app = FastAPI(
    title='Ensaware',
    version='0.0.1',
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=tuple(settings.cors_origins.split(',')),
    allow_credentials=True,
    allow_methods=tuple(settings.cors_methods.split(',')),
    allow_headers=["*"],
)
app.exception_handler(EnsawareException)(ensaware_exception_handler.ensaware)

add_pagination(app)


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