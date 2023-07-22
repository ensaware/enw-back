import requests


class BookResponse:
    title: str
    subtitle: str | None
    isbn_13: str
    isbn_10: str | None


class Book:
    def __init__(self) -> None:
        self.__url = 'https://openlibrary.org'


    def isbn(self, code: str) -> BookResponse:
        if not code:
            raise ValueError('Asegúrese de enviar un código ISBN valido.')
        
        response = requests.get(f'{self.__url}/isbn/{code}.json')

        if response.status_code == 404:
            raise ValueError('ISBN no encontrado.')
        
        response_json: dict = response.json()
        book_reponse: BookResponse = BookResponse()

        book_reponse.title = response_json.get('title', None)
        book_reponse.subtitle = response_json.get('subtitle', None)

        if 'isbn_13' in response_json:
            book_reponse.isbn_13 = response_json['isbn_13'][0]
        else:
            book_reponse.isbn_13 = None

        if 'isbn_10' in response_json:
            book_reponse.isbn_10 = response_json['isbn_10'][0]
        else:
            book_reponse.isbn_10 = None

        return book_reponse