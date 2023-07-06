import logging

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from authorization.v1.schema import Token, RefreshToken
from utils import replace_url_scheme
from utils.oauth.provider import Provider, SelectProvider
from utils.database import get_db
from utils.exception.ensaware import EnsawareException
from utils.settings import Settings


router = APIRouter()
settings = Settings()


@router.get(
    '/{provider}',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
def login_provider(
    request: Request,
    provider: Provider,
    db: Session = Depends(get_db)
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

    redirect_url, _ = SelectProvider.select(provider, url, db).authentication()

    return RedirectResponse(redirect_url)


@router.get(
    '/{provider}/auth',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_model=Token
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

    redirect_url: str = SelectProvider.select(provider, url, db).get_data(request)

    return RedirectResponse(redirect_url)


@router.post(
    '/{provider}/refresh/token',
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
def refresh_token(
    provider: Provider,
    refresh_token: RefreshToken,
    db: Session = Depends(get_db)
):
    '''
    Actualizar token vencido.

    ### Return
    - `Token class` Respuesta del proveedor donde se entrege el token, token_type y refresh_token.
    '''
    try:
        return SelectProvider.select(provider, '', db).refresh_token(refresh_token.refresh_token)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw