from abc import ABC, abstractmethod

from utils.encryption import Encryption


class Auth20(ABC):
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