from fastapi import status
from sqlalchemy.orm import Session

from utils.http.book import BookResponse

from . import models, schema


def create_library(db: Session, book_response: BookResponse) -> schema.Library:
    book = get_book_isbn_13(db, book_response.isbn_13)
    if book:
        return book
    
    book = get_book_isbn_10(db, book_response.isbn_13)
    if book:
        return book
    
    db_book = models.Library(
        title = book_response.title,
        subtitle = book_response.subtitle,
        isbn_13 = book_response.isbn_13,
        isbn_10 = book_response.isbn_10
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return schema.Library.model_validate(db_book)


def create_library_user(db: Session, book_id: str, user_id: str) -> schema.LibraryUser:
    db_library_user = models.LibraryUser(
        library_id = book_id,
        user_id = user_id
    )

    db.add(db_library_user)
    db.commit()
    db.refresh(db_library_user)

    return schema.LibraryUser.model_validate(db_library_user)


def get_all(db: Session) -> list[schema.LibraryUser]:
    return db.query(models.LibraryUser).\
            order_by(models.LibraryUser.created.desc())


def get_book_isbn_10(db: Session, isbn: str) -> schema.Library:
    book = db.query(models.Library).\
            filter(models.Library.isbn_10 == isbn).\
            first()
    
    if book:
        return schema.Library.model_validate(book)
    else:
        return None


def get_book_isbn_13(db: Session, isbn: str) -> schema.Library | None:
    book = db.query(models.Library).\
            filter(models.Library.isbn_13 == isbn).\
            first()
    
    if book:
        return schema.Library.model_validate(book)
    else:
        return None
    

def get_user_id(db: Session, id: str) -> list[schema.LibraryUser]:
    user = db.query(models.LibraryUser).\
            filter(models.LibraryUser.user_id == id).\
            order_by(models.LibraryUser.created.desc())
    
    return user