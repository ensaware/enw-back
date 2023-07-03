import logging

from fastapi import APIRouter, Depends, status, Response, UploadFile
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import Field
from sqlalchemy.orm import Session
from typing import Union


from exception.ensaware import EnsawareException
from oauth.security import Security
from user.v1 import schema
from user.v1.schema import TokenData
from utils.database import ENGINE, get_db

from . import QR
from . import crud, models, schema


Page = Page.with_custom_options(
    size=Field(10, ge=1)
)


router = APIRouter(
    dependencies=[Depends(Security.get_token)],
)
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
    response_model=Page [schema.HistoricQrCode]
)
def historic(
    token: TokenData = get_token,
    db: Session = Depends(get_db),
):
    try:
        return paginate(crud.get_historic_qr_code_user_id(db, token.sub))
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw


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
    response_model=str
)
async def read_imagen(
    image: UploadFile,
    db: Session = Depends(get_db),
):
    try:
        contents = await image.read()
        result = QR(db)

        return result.read_image(contents)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw