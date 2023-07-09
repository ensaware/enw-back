from enum import Enum, unique


@unique
class Error(Enum):
    QR_CODE_READ = 'Error al leer la información del código QR.'
    QR_CODE_AUTH = 'No estás autorizado(a) para leer el código QR.'
    FAILED_CREATE_JWT = 'Error al crear el token.'
    EXPIRED_TOKEN = 'Token expirado.'
    REFRESH_TOKEN_FAILED = 'No se puedo actulizar el token. Asegúrese de enviar el refresh token correcto.'


@unique
class Validate(Enum):
    INVALID_AUTH = 'No esta autorizado para realizar esta solicitud.'
    INVALID_EMAIL = 'Corre electrónico invalido.'
    INVALID_PROVIDER = 'Proveedor no valido.'
    INVALID_JWT = 'Token no valido.'
    INVALID_REFRESH_TOKEN = 'refresh token no válido.'
    INVALID_USER = 'Usuario no válido.'
    INVALID_QR_CODE_CREATE = 'Error al crear el código qr.'


@unique
class TypeMessage(Enum):
    ERROR = 'ERROR'
    INFORMATION = 'INFORMATION'
    WARNING = 'WARNING'
    VALIDATION = 'VALIDATION'