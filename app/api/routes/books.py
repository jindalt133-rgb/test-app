from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
) -> BookResponse:
    return BookService(db).create_book(book_data)


@router.get("", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)) -> list[BookResponse]:
    return BookService(db).list_books()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
) -> BookResponse:
    return BookService(db).get_book(book_id)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
) -> BookResponse:
    return BookService(db).update_book(book_id, book_data)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
) -> Response:
    BookService(db).delete_book(book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
