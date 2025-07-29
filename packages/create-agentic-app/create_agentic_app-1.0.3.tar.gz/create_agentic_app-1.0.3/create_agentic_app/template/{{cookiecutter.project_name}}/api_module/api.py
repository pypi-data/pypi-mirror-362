from typing import List

from fastapi import APIRouter, status, HTTPException

from .model import Book, BookCreate
from .service import BookCrud

api_router = APIRouter()
book_crud = BookCrud()


@api_router.get("/book", response_model=List[Book])
async def get_books():
    return book_crud.get_books()


@api_router.get("/book/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    book = book_crud.get_book_by_id(book_id)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@api_router.post("/book", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    return book_crud.create_book(book)
