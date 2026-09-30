"""Book catalog API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.books import BookCreate, BookResponse, BookUpdate
from app.services import books as book_service

router = APIRouter(prefix="/books", tags=["books"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, session: DatabaseSession) -> BookResponse:
    return book_service.create_book(session, payload)


@router.get("", response_model=list[BookResponse])
def list_books(session: DatabaseSession, query: Annotated[str | None, Query(alias="q", description="Search title or author")] = None) -> list[BookResponse]:
    return book_service.list_books(session, query)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, session: DatabaseSession) -> BookResponse:
    return book_service.get_book(session, book_id)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, payload: BookUpdate, session: DatabaseSession) -> BookResponse:
    return book_service.update_book(session, book_id, payload)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, session: DatabaseSession) -> Response:
    book_service.delete_book(session, book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)