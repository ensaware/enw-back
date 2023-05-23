from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel


class EnsawareException(Exception):
    def __init__(self, status_code: int, type: str, message: str) -> None:
        self.message = message
        self.status_code = status_code
        self.type = type

        super().__init__(self.message)


class EnsawareExceptionBase(BaseModel):
    code: str
    message: str
    type: str


class EnsawareExceptionHandler:
    def ensaware(self, request: Request, enw: EnsawareException):
        enw_base = EnsawareExceptionBase(
            code=enw.status_code,
            message=enw.message,
            type=enw.type
        )

        return JSONResponse(
            status_code=enw.status_code,
            content=enw_base.dict()
        )