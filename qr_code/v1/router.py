from fastapi import APIRouter, Depends, status, Request, Response, UploadFile
from sqlalchemy.orm import Session
from typing import Union

from utils.database import ENGINE, get_db
from . import QR
from . import crud, models, schema



router = APIRouter()
models.Base.metadata.create_all(bind=ENGINE)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    summary='Prueba',
    response_model=schema.QRCode
)
def create_qr_code(
    qr_code: schema.QRCodeBase,
    db: Session = Depends(get_db)
):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return crud.create_qr_code(
        db,
        qr_code
    )


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schema.QRCode,
    responses={
        204: {'model': None}
    }
)
def get_qr_code(
    id: str,
    response: Response,
    db: Session = Depends(get_db),
):
    qr_code = crud.get_qr_code(
        db,
        id
    )

    if qr_code:
        return qr_code
    
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get(
    '/{email}/generate',
    status_code=status.HTTP_200_OK,
)
def qr_code_generate(
    request: Request,
    email: str,
    background: Union[str, None] = None,
    color: Union[str, None] = None,
    show_logo: bool = True,
    db: Session = Depends(get_db),
):
    url = str(request.base_url)
    result = QR(db)
    qr = result.generate(email, url, show_logo, background, color)
    
    return Response(content=qr, media_type='image/png')


@router.get(
    '/{email}/read',
    status_code=status.HTTP_200_OK,
    response_model=schema.QRCode,
)
def qr_code_read(
    email: str,
    token: str,
    db: Session = Depends(get_db),
):
    result = QR(db)
    return result.read(email, token)


@router.post(
    '/{email}/read',
    status_code=status.HTTP_200_OK,
    response_model=schema.QRCode,
)
async def qr_code_read_imagen(
    email: str,
    image: UploadFile,
    db: Session = Depends(get_db),
):
    contents = await image.read()
    result = QR(db)
    return result.read_imagen(email, contents)