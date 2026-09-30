from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, service: BookService = Depends(get_book_service)) -> BookRead:
    return service.create_book(payload)


@router.get("", response_model=list[BookRead])
def list_books(service: BookService = Depends(get_book_service)) -> list[BookRead]:
    return service.list_books()


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int = Path(..., ge=1), service: BookService = Depends(get_book_service)) -> BookRead:
    return service.get_book(book_id)


@router.put("/{book_id}", response_model=BookRead)
def update_book(payload: BookUpdate, book_id: int = Path(..., ge=1), service: BookService = Depends(get_book_service)) -> BookRead:
    return service.update_book(book_id, payload)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(..., ge=1), service: BookService = Depends(get_book_service)) -> None:
    service.delete_book(book_id)
