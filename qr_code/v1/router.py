import logging

from fastapi import APIRouter, Depends, status, Request, Response, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Union


from exception.ensaware import EnsawareException, EnsawareExceptionBase
from user.v1 import DecryptedToken, schema
from user.v1.schema import TokenData
from utils import replace_url_scheme
from utils.database import ENGINE, get_db
from utils.settings import Settings

from . import QR
from . import models, schema



router = APIRouter(
    dependencies=[Depends(DecryptedToken.get_token)],
    responses={
        400: {
            'model': EnsawareExceptionBase
        },
        401: {
            'model': EnsawareExceptionBase
        }
    },
)
settings = Settings()
models.Base.metadata.create_all(bind=ENGINE)

get_token = router.dependencies[0]


@router.get(
    '/generate',
    status_code=status.HTTP_200_OK,
)
def generate(
    token: TokenData = get_token,
    background: Union[str, None] = None,
    color: Union[str, None] = None,
    show_logo: bool = True,
    db: Session = Depends(get_db),
):
    try:
        result = QR(db)
        qr = result.generate(token.sub, show_logo, background, color)

        return Response(content=qr, media_type='image/png')
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw
    

@router.get(
    '/historic',
    status_code=status.HTTP_200_OK,
)
def generate(
    token: TokenData = get_token,
    db: Session = Depends(get_db),
):
    return token


@router.get(
    '/read',
    status_code=status.HTTP_200_OK,
    response_model=schema.UserHistory,
)
def qr_code_read(
    token: str,
    token_data: TokenData = get_token,
    db: Session = Depends(get_db),
):
    try:
        result = QR(db)
        return result.read(token_data, token)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw


@router.post(
    '/read/image',
    status_code=status.HTTP_303_SEE_OTHER,
)
async def read_imagen(
    request: Request,
    image: UploadFile,
    db: Session = Depends(get_db),
):
    try:
        contents = await image.read()
        result = QR(db)
        token_id = result.read_image(contents)

        index: int = str(request.url).index('/image')
        url: str = f'{str(request.url)[0: index]}/?token={token_id}'

        if settings.debug == 0:
            url = replace_url_scheme(url)

        return RedirectResponse(url, status.HTTP_303_SEE_OTHER)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw