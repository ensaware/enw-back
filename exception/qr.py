from . import Error, TypeMessage, Validate

class QRCodeError(Exception):
    def __init__(self, message: Error) -> None:
        self.type = TypeMessage.ERROR.name
        self.message = message.value
        super().__init__(self.message)


class QRCodeValidate(Exception):
    def __init__(self, message: Validate) -> None:
        self.type = TypeMessage.VALIDATION.name
        self.message = message.value
        super().__init__(self.message)