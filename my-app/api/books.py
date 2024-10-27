
from sqlmodel import Field, create_engine, select
from fastapi import Depends, HTTPException, Query, Response
from typing import Annotated
from datetime import datetime
from models.books import BookBase
# , BookUpdate
from models.reviews import ReviewBase
from db.utils import SessionDep, logger
from fastapi import APIRouter
import requests
import time

router = APIRouter()

# add new books
@router.post("/books/", response_model=BookBase)
async def create_book(book: BookBase, session: SessionDep):
    db_book = BookBase.model_validate(book)
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book

# get books
@router.get("/books/", response_model=list[BookBase])
async def get_all_books(
    session: SessionDep,
):
    statement = select(BookBase)
    books = await session.exec(statement=statement)
    return books

# get reviews
@router.get("/books/reviews", response_model=list[ReviewBase])
async def get_all_reviews(
    session: SessionDep
    ):
    statement = select(ReviewBase)
    rev = await session.exec(statement=statement)
    return rev

# get books by id
@router.get("/books/{id}", response_model=BookBase)
async def get_book_by_id(id: int, session: SessionDep):
    statement = select(BookBase).where(BookBase.id == id)
    book = await session.exec(statement=statement)
    # res = book.scalar_one_or_none() 
    book = book.one_or_none()
    logger.warning(book)
    if book is None: 
        raise HTTPException(status_code=404, detail="Book not found")
    return book
    

#  update book data
@router.patch("/books/{id}", response_model=BookBase)
async def update_book(id: int, book: BookBase, session: SessionDep):
    db_book = BookBase.model_validate(book)
    logger.warning('header')
    logger.warning(book)
    statement = select(BookBase).where(BookBase.id == id)
    db_book = await session.exec(statement=statement)
    db_book = db_book.one_or_none()
    logger.warning('old')
    logger.info(db_book)
    if db_book is None: 
        raise HTTPException(status_code=404, detail="Book not found")
    values = book.model_dump(exclude_unset=True, context = BookBase)
    for k, v in values.items():
        logger.info(f'{k} -- {v}')
        if k == 'year_published':
            v = datetime.strptime(v, '%Y-%m-%d').date()
        setattr(db_book, k, v)
    # book_data = book.model_dump(exclude_unset=True)
    logger.warning('new')
    logger.warning(db_book)
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
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

@router.get('/ask')
async def ask(prompt :str):
    context = 'Summarize the content: '
    res = requests.post('http://localhost:11434/api/generate', json={
        "prompt": context + prompt,
        "stream" : False,
        "model" : "qwen2.5:1.5b"
    })

    return {"summary": res.json()['response']}








