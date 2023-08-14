import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from authorization.v1.schema import TokenData
from utils.database import get_db
from utils.exception.ensaware import EnsawareException
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


@router.get(
    '/all',
    response_model=list[schema.Career],
    status_code=status.HTTP_200_OK,
)
def all(
    token: TokenData = get_token,
    # authorize: bool = Depends(PermissionChecker(code_name='user:read:all')),
    db: Session = get_db
):
    try:
        return crud.get_career(db)
    except EnsawareException as enw:
        logging.exception(enw)
        raise enw