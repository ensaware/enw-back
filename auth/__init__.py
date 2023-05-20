from abc import ABC, abstractmethod


class Auth20(ABC):
    def __init__(self, url_callback: str) -> None:
        self.url_callback = url_callback

    @abstractmethod
    def authentication(self):
        pass


    @abstractmethod
    def get_data(self):
        pass