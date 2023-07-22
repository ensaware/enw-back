import logging

from fastapi import APIRouter, Depends, status, UploadFile
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from . import crud, schema
from authorization.v1.schema import TokenData
from utils.database import get_db
from utils.exception.ensaware import EnsawareException
from utils.http.book import Book
from utils.oauth.security import Security
from utils.quick_response_code.barcode import BarCode


router = APIRouter(
    dependencies=[
        Depends(Security.get_token),
        Depends(get_db)
    ]
)

get_token = router.dependencies[0]
get_db = router.dependencies[1]


@router.get(
    '',
    response_model=Page[schema.LibraryUser],
    status_code=status.HTTP_200_OK,
)
def library(
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        return paginate(crud.get_user_id(db, token.sub))
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw
    

@router.get(
    '/see/all',
    response_model=Page[schema.LibraryUser],
    status_code=status.HTTP_200_OK,
)
def see_all(
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        return paginate(crud.get_all(db))
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw
    

@router.get(
    '/{user_id}',
    response_model=Page[schema.LibraryUser],
    status_code=status.HTTP_200_OK,
)
def user_id(
    user_id: str,
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        return paginate(crud.get_user_id(db, user_id))
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw


@router.post(
    '/read/image',
    response_model=schema.LibraryUser,
    status_code=status.HTTP_200_OK
)
async def read_imagen(
    image: UploadFile,
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        contents = await image.read()
        barcode = BarCode()
        isbn = barcode.read(contents)
        book = Book()
        book_response = book.isbn(isbn)
        
        create_book = crud.create_library(db, book_response)
        return crud.create_library_user(db, create_book.id, token.sub)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw