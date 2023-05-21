from enum import Enum, unique

from exception.provider import ProviderValidate, Validate
from .google import GoogleProvider


@unique
class Provider(Enum):
    GOOGLE = 'google'


class SelectProvider:
    @staticmethod
    def select(provider: Provider, url_callback: str):
        if provider == Provider.GOOGLE:
            return GoogleProvider(url_callback)
        else:
            raise ProviderValidate(Validate.INVALID_PROVIDER)