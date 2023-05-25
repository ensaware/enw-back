from urllib.parse import urlparse


def replace_url_scheme(url: str):
    scheme: str = urlparse(url).scheme

    if scheme.lower() == 'http':
        return url.replace('http', 'https')
    
    return url