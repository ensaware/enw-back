import logging

from fastapi import APIRouter, Depends, status, Response, UploadFile
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from typing import Union

from . import crud, schema
from authorization.v1.schema import TokenData
from utils.database import get_db
from utils.exception.ensaware import EnsawareException
from utils.oauth.security import Security
from utils.quick_response_code.qr import QRCode


router = APIRouter(
    dependencies=[
        Depends(Security.get_token),
        Depends(get_db)
    ],
)

get_token = router.dependencies[0]
get_db = router.dependencies[1]


@router.get(
    '/create',
    status_code=status.HTTP_200_OK,
)
def create(
    token: TokenData = get_token,
    background: Union[str, None] = None,
    color: Union[str, None] = None,
    show_cua_logo: bool = True,
    db: Session = get_db
):
    try:
        result = QRCode(db, token.sub, background, color, show_cua_logo)
        qr = result.create()

        return Response(content=qr, media_type='image/png')
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw
    

@router.get(
    '/historic',
    status_code=status.HTTP_200_OK,
    response_model=Page[schema.HistoricQrCode]
)
def historic(
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        return paginate(crud.get_historic_qr_code_user_id(db, token.sub))
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw


@router.post(
    '/read/image',
    status_code=status.HTTP_200_OK,
    response_model=schema.HistoricQrCode,
)
async def read_imagen(
    image: UploadFile,
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        contents = await image.read()
        result = QRCode(db, token.sub)

        return result.read(contents)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw