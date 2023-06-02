import logging

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from auth.provider import Provider, SelectProvider
from exception.ensaware import EnsawareException, EnsawareExceptionBase
from utils import replace_url_scheme
from utils.database import ENGINE, get_db
from utils.settings import Settings
from . import crud, models, schema, DecryptedToken


router = APIRouter()
settings = Settings()
models.Base.metadata.create_all(bind=ENGINE)


@router.get(
    '/login/{provider}',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
def login_provider(
    request: Request,
    provider: Provider
):
    '''
    Permite iniciar sessión a través de OAuth.

    - `provider` Nombre del proveedor.

    Redirecciona a la url del proveedor para pedir autorización al usuario.

    **Importante:** Por el momento solo se tiene el proveedor Google.
    '''
    url: str = f'{str(request.url)}/auth'

    if settings.debug == 0:
        url = replace_url_scheme(url)

    redirect_url, _ = SelectProvider.select(provider, url).authentication()

    return RedirectResponse(redirect_url)


@router.get(
    '/login/{provider}/auth',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_model=schema.Token
)
def login_provider_auth(
    request: Request,
    provider: Provider,
    db: Session = Depends(get_db)
):
    '''
    callback URL con la respuesta del proveedor.

    - `provider` Nombre del proveedor.

    ### Return
    - `Token class` Respuesta del proveedor donde se entrege el token, token_type y refresh_token.

    **Importante:** Por el momento solo se tiene el proveedor Google.
    '''
    index: int = str(request.url).index('?')
    url: str = str(request.url)[0: index]

    if settings.debug == 0:
        url = replace_url_scheme(url)

    redirect_url: str = SelectProvider.select(provider, url).get_data(db, request)

    return RedirectResponse(redirect_url)


@router.get(
    '/me',
    responses={
        401: {
            'model': EnsawareExceptionBase
        }
    },
    response_model=schema.User,
    status_code=status.HTTP_200_OK,
)
def user_me(
    token: schema.TokenData = Depends(DecryptedToken.get_token),
    db: Session = Depends(get_db)
):
    '''
    Entrega información del usuario.

    **Nota:** Se debe de enviar en el encabezado el token del usuario.
    '''
    try:
        return crud.get_user_id(db, token.sub)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw
    

@router.post(
    '/refresh/token/{provider}',
    responses={
        400: {
            'model': EnsawareExceptionBase
        }
    },
    response_model=schema.Token,
    status_code=status.HTTP_200_OK,
)
def refresh_token(
    provider: Provider,
    refresh_token: schema.RefreshToken,
    db: Session = Depends(get_db)
):
    '''
    Actualizar token vencido.

    ### Return
    - `Token class` Respuesta del proveedor donde se entrege el token, token_type y refresh_token.
    '''
    try:
        return SelectProvider.select(provider, '').refresh_token(db, refresh_token.refresh_token)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw
