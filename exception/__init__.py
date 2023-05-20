from enum import Enum, unique


@unique
class Error(Enum):
    QR_CODE_READ = 'Error leyendo la información del código QR.'
    QR_CODE_EMAIL = 'El correo electrónico no pertenece al código QR.'


@unique
class Validate(Enum):
    INVALID_EMAIL = 'Corre electrónico invalido.'
    INVALID_PROVIDER = 'Proveedor no valido.'


@unique
class TypeMessage(Enum):
    ERROR = 'ERROR'
    INFORMATION = 'INFORMATION'
    WARNING = 'WARNING'
    VALIDATION = 'VALIDATION'