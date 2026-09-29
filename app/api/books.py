from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session
from app.dependencies import database_session
from app.schemas import BookCreate, BookResponse, BookUpdate
from app.services import book_service

router = APIRouter(prefix="/books", tags=["books"])
DatabaseSession = Annotated[Session, Depends(database_session)]

@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: DatabaseSession) -> BookResponse: return book_service.create_book(db, payload)
@router.get("", response_model=list[BookResponse])
def list_books(db: DatabaseSession, q: str | None = Query(default=None, description="Search title or author")) -> list[BookResponse]: return book_service.list_books(db, q)
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: DatabaseSession) -> BookResponse: return book_service.get_book(db, book_id)
@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, payload: BookUpdate, db: DatabaseSession) -> BookResponse: return book_service.update_book(db, book_id, payload)
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: DatabaseSession) -> Response:
    book_service.delete_book(db, book_id); return Response(status_code=status.HTTP_204_NO_CONTENT)