from urllib.parse import urlparse, ParseResult


def replace_url_scheme(url: str):
    _urlparse: ParseResult = urlparse(url)
    scheme: str = _urlparse.scheme.lower()
    hostname: str = _urlparse.hostname.lower()

    if hostname == 'localhost':
        return url

    if scheme == 'http':
        return url.replace('http', 'https')
    
    return url