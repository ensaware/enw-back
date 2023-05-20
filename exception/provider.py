from . import Error, TypeMessage, Validate


class ProviderValidate(Exception):
    def __init__(self, message: Validate) -> None:
        self.type = TypeMessage.VALIDATION.name
        self.message = message.value
        super().__init__(self.message)