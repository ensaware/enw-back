import logging

from fastapi import APIRouter, Depends, status
from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from authorization.v1.schema import TokenData
from utils.database import get_db
from utils.exception.ensaware import EnsawareException
from utils.oauth import PermissionChecker
from utils.oauth.security import Security
from . import crud, schema


router = APIRouter(
    dependencies=[
        Depends(Security.get_token),
        Depends(get_db)
    ]
)

get_token = router.dependencies[0]
get_db = router.dependencies[1]


@router.delete(
    '/{id}',
    response_model=schema.UserRead,
    status_code=status.HTTP_200_OK,
)
def delete_user_id(
    id: str,
    # authorize: bool = Depends(PermissionChecker(code_name='user:delete:all')),
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        return crud.delete_user_id(db, id, True)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw


@router.get(
    '/{id}',
    response_model=schema.UserRead,
    status_code=status.HTTP_200_OK,
)
def user_id(
    id: str,
    # authorize: bool = Depends(PermissionChecker(code_name='user:read:all')),
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        return crud.get_user_id(db, id, True)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw
    

@router.patch(
    '/{id}',
    response_model=schema.UserRead,
    status_code=status.HTTP_200_OK,
)
def update_user_id(
    id: str,
    update_user: schema.UserUpdate,
    # authorize: bool = Depends(PermissionChecker(code_name='user:update:all')),
    token: TokenData = get_token,
    db: Session = get_db
):
    try:
        user_model = crud.get_user_id(db, id)
        updated_user = user_model.model_copy(update=update_user.dict(exclude_unset=True))

        return crud.update_user_id(db, id, updated_user, True)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw


@router.get(
    '/see/all',
    response_model=Page[schema.UserRead],
    status_code=status.HTTP_200_OK,
)
def see_all_users(
    token: TokenData = get_token,
    # authorize: bool = Depends(PermissionChecker(code_name='user:read:all')),
    db: Session = get_db
):
    try:
        return paginate(crud.get_user_all(db))
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw


@router.get(
    '',
    response_model=schema.UserRead,
    status_code=status.HTTP_200_OK,
)
def user_me(
    token: TokenData = get_token,
    # authorize: bool = Depends(PermissionChecker(code_name='user:read')),
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
    '',
    response_model=schema.UserRead,
    status_code=status.HTTP_200_OK,
)
def update_user_me(
    update_user: schema.UserUpdate,
    token: TokenData = get_token,
    # authorize: bool = Depends(PermissionChecker(code_name='user:update')),
    db: Session = get_db
):
    try:
        user_model = crud.get_user_id(db, token.sub)
        updated_user = user_model.model_copy(update=update_user.model_dump(exclude_unset=True))

        return crud.update_user_id(db, token.sub, updated_user, True)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw