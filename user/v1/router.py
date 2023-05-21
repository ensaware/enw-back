from fastapi import APIRouter, Depends, Header, status, Request, Response, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Annotated

from auth.provider import Provider, SelectProvider
from utils.database import ENGINE, get_db

from . import crud, JWT, models, schema


router = APIRouter()
models.Base.metadata.create_all(bind=ENGINE)
oauth2_token = HTTPBearer()
jwt = JWT()


@router.get(
    '/login/{provider}',
    status_code=status.HTTP_200_OK
)
def login_provider(
    request: Request,
    provider: Provider,
):
    url: str = f'{str(request.url)}/auth'
    redirect_url, _ = SelectProvider.select(provider, url).authentication()

    return RedirectResponse(redirect_url)


@router.get(
    '/login/{provider}/auth',
    status_code=status.HTTP_200_OK,
    response_model=schema.Token
)
def login_provider(
    request: Request,
    provider: Provider,
    code: str,
    db: Session = Depends(get_db)
):
    index: int = str(request.url).index('?')
    url: str = str(request.url)[0: index]
    token: schema.Token = SelectProvider.select(provider, url).get_data(db, request)

    return RedirectResponse(
        url = '/v1/user/me',
         headers = {
            'Authorization': f'{token.token_type} {token.token}'
        }
    )


@router.get(
    '/me',
    response_model=schema.User,
    status_code=status.HTTP_200_OK
)
def user_me(
    token: Annotated[str, Depends(oauth2_token)],
    db: Session = Depends(get_db)
):
    token_data: schema.TokenData = jwt.decode(token.credentials)
    return crud.get_user_id(db, token_data.sub)