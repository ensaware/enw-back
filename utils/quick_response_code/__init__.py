from abc import ABC, abstractmethod


class CreateQuickResponseCode(ABC):
    @abstractmethod
    def create(self) -> bytes:
        pass


class ReadQuickResponseCode(ABC):
    @abstractmethod
    def read(self, image: bytes) -> any:
        pass