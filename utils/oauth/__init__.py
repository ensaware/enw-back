from abc import ABC, abstractmethod

from utils.encryption import Encryption


class OAuth20(ABC):
    def __init__(self, url_callback: str) -> None:
        self.url_callback: str = url_callback
        self.encryption: Encryption = Encryption()

    @abstractmethod
    def authentication(self):
        pass


    @abstractmethod
    def get_data(self):
        pass


    @abstractmethod
    def refresh_token(self):
        pass


# class PermissionChecker:
#     def __init__(self, required_permissions: list[str]) -> None:
#         self.required_permissions = required_permissions

#     def __call__(self, user: PyUser = Depends(get_current_user)) -> bool:
#         for r_perm in self.required_permissions:
#             if r_perm not in user.permissions:
#                 raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail='Permissions'
#                 )
#         return True