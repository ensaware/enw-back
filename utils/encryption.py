from cryptography.fernet import Fernet

from utils.settings import Settings


class Encryption:
    def __init__(self) -> None:
        self._settings: Settings = Settings()
        self._fernet_pass: str = self._settings.fernet_pass
        self._fernet: Fernet = Fernet(self._fernet_pass)
        self._encode: str = self._settings.encode


    def encrypt(self, message: str) -> str:
        return self._fernet.encrypt(message.encode(self._encode)).decode(self._encode)
    

    def decrypt(self, token: str) -> str:
        return self._fernet.decrypt(token).decode(self._encode)