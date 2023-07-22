import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from authorization.v1.router import router as authorization
from library.v1.router import router as library
from qr_code.v1.router import router as qr_code
from utils.exception.ensaware import EnsawareException, EnsawareExceptionBase, EnsawareExceptionHandler
from user.v1.router import router as user
from utils.settings import Settings


# Se deja habilitado hasta tener un dominio con el protocolo https
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


settings = Settings()
ensaware_exception_handler = EnsawareExceptionHandler()


app = FastAPI(
    title='Ensaware',
    version='0.0.1',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    responses={
        400: {
            'model': EnsawareExceptionBase
        },
        401: {
            'model': EnsawareExceptionBase
        }
    },
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
    authorization,
    prefix='/v1/authorization',
    tags=['v1 - authorization']
)

app.include_router(
    library,
    prefix='/v1/library',
    tags=['v1 - library']
)

app.include_router(
    qr_code,
    prefix='/v1/qr-code',
    tags=['v1 - qr code'],
)

app.include_router(
    user,
    prefix='/v1/user',
    tags=['v1 - user']
)