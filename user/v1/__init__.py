from enum import Enum, unique


@unique
class ProfileType(Enum):
    STUDENT = 'estudiante'
    TEACHER = 'profesor'
    ADMINISTRATIVE = 'administrativo'
    ADMINISTRATOR = 'administrador'