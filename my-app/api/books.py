
from sqlmodel import Field, create_engine, select
from fastapi import Depends, HTTPException, Query
from typing import Annotated
from models.books import BookBase, BookUpdate
from models.reviews import ReviewBase
from db.utils import SessionDep
from fastapi import APIRouter

router = APIRouter()

# add new books
@router.post("/books/", response_model=BookBase)
async def create_book(book: BookBase, session: SessionDep):
    db_book = BookBase.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# get books
@router.get("/books/", response_model=list[BookBase])
async def get_all_books(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    books = session.exec(select(BookBase).offset(offset).limit(limit)).all()
    return books

# get reviews
@router.get("/books/reviews", response_model=list[ReviewBase])
async def get_all_reviews(
    session: SessionDep
    ):
    rev = session.exec(select(ReviewBase)).all()
    return rev

# get books by id
@router.get("/books/{id}", response_model=BookBase)
async def get_book_by_id(id: int, session: SessionDep):
    book = session.get(BookBase, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


#  update book data
@router.patch("/books/{id}", response_model=BookBase)
async def update_book(id: int, book: BookUpdate, session: SessionDep):
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
async def delete_book(id: int, session: SessionDep) :
    book = session.get(BookBase, id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}

# POST /books/<id>/reviews: Add a review for a book.

@router.post("/books/{id}/reviews", response_model=None)
async def add_reviews(id: int, review: ReviewBase, session: SessionDep):
    book = session.get(BookBase, id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    
    # do similar to check user_id exist or not

    # book = session.get(BookBase, id)
    # if not book:
    #     raise HTTPException(status_code=404, detail="book not found")


    review.book_id = id
    db_review = ReviewBase.model_validate(review)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@router.get("/books/{id}/reviews", response_model=list[ReviewBase])
async def get_reviews_by_id(id: int, session: SessionDep):

    reviews = session.exec(select(ReviewBase).where(ReviewBase.book_id == id))
    return reviews

@router.get("/books/{id}/summary", response_model=None)
async def get_summary_review(id: int, session: SessionDep):
    
    reviews = session.exec(select(ReviewBase.rating).where(ReviewBase.book_id == id))
    summary = session.exec(select(BookBase.summary).where(BookBase.id == id))
    li = []
    for rev in reviews:
        li.append(rev)
    li_ = []
    for sum_ in summary:
        li_.append(sum_)
    average_rating = sum(li)/len(li)
    return {"summary": li_,
            "msg": average_rating}




