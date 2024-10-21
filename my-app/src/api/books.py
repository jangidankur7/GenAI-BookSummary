
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends, FastAPI, HTTPException, Query
from typing import Annotated
from models.books import BookBase, BookUpdate
from models.reviews import ReviewBase
from db.utils import SessionDep
from fastapi import APIRouter
from main import logger

router = APIRouter()

# add new books
@router.post("/books/", response_model=BookBase)
def create_book(book: BookBase, session: SessionDep):
    db_book = BookBase.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# get books
@router.get("/books/", response_model=list[BookBase])
def get_all_books(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    books = session.exec(select(BookBase).offset(offset).limit(limit)).all()
    return books

# get books by id
@router.get("/books/{id}", response_model=BookBase)
def get_book_by_id(id: int, session: SessionDep):
    book = session.get(BookBase, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


#  update book data
@router.patch("/books/{id}", response_model=BookBase)
def update_book(id: int, book: BookUpdate, session: SessionDep):
        db_book = session.get(BookBase, id)
        if not db_book:
            raise HTTPException(status_code=404, detail="book not found")
        book_data = book.model_dump(exclude_unset=True)
        db_book.sqlmodel_update(book_data)
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book

@router.delete("/books/{id}")
def delete_book(id: int, session: SessionDep) :
    book = session.get(BookBase, id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}

# POST /books/<id>/reviews: Add a review for a book.

# @router.post("/books/{id}/reviews", response_model=ReviewBase)
# def create_book(review: ReviewBase, session: SessionDep):
#     db_review = BookBase.model_validate(review)
#     session.add(db_review)
#     session.commit()
#     session.refresh(db_review)
#     return db_review


