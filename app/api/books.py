from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.book import BookInput, BookResponse
from app.services.book_service import BookService

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

Database = Annotated[
    Session,
    Depends(get_db),
]


@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    data: BookInput,
    db: Database,
) -> BookResponse:
    return BookService(db).create(data)


@router.get(
    "",
    response_model=list[BookResponse],
)
def get_books(db: Database) -> list[BookResponse]:
    return BookService(db).list_all()


@router.get(
    "/search",
    response_model=list[BookResponse],
)
def search_books(
    db: Database,
    q: Annotated[str, Query(min_length=1)],
) -> list[BookResponse]:
    return BookService(db).search(q)


@router.get(
    "/{book_id}",
    response_model=BookResponse,
)
def get_book(
    book_id: int,
    db: Database,
) -> BookResponse:
    return BookService(db).get(book_id)


@router.put(
    "/{book_id}",
    response_model=BookResponse,
)
def update_book(
    book_id: int,
    data: BookInput,
    db: Database,
) -> BookResponse:
    return BookService(db).update(book_id, data)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(
    book_id: int,
    db: Database,
) -> Response:
    BookService(db).delete(book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)