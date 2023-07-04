import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from authorization.v1.schema import TokenData
from exception.ensaware import EnsawareException
from oauth.security import Security
from utils.database import get_db
from utils.settings import Settings
from . import crud, schema


router = APIRouter(
    dependencies=[
        Depends(Security.get_token),
        Depends(get_db)
    ],
)

settings = Settings()

get_token = router.dependencies[0]
get_db = router.dependencies[1]


@router.get(
    '/me',
    response_model=schema.UserRead,
    status_code=status.HTTP_200_OK,
)
def user_me(
    token: TokenData = get_token,
    db: Session = get_db
):
    '''
    Entrega información del usuario.

    **Nota:** Se debe de enviar en el encabezado el token del usuario.
    '''
    try:
        return crud.get_user_id(db, token.sub, True)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw
    

@router.patch(
    '/me',
    response_model=schema.UserRead,
    status_code=status.HTTP_200_OK,
)
def user_update_me(
    update_user: schema.UserUpdate,
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        user_model = crud.get_user_id(db, token.sub)
        updated_user = user_model.copy(update=update_user.dict(exclude_unset=True))

        return crud.update_user_id(db, token.sub, updated_user, True)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw