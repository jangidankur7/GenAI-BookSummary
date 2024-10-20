import os
import dotenv
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
import json
import logging
from datetime import datetime

logger = logging.getLogger('uvicorn.error')

dotenv.load_dotenv('/root/GenAI-BookSummary/my-app/.env')
POSTGRES_URI = os.getenv('POSTGRES_URI')

class BookBase(SQLModel, table=True):
    __tablename__ = "books"
    id: int  | None = Field(index=True, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    genre: str = Field(index=True)
    year_published: datetime = Field(index=True)
    summary: str | None = Field(default=None, index=True)



class ReviewBase(SQLModel, table=True):
    __tablename__ = "reviews"
    id: int| None = Field(index=True, primary_key=True)
    book_id: int = Field(index=True, foreign_key="books.id")
    user_id: int | None = Field(default=None)
    review_text : str | None = Field(default=None)
    review_text : int = Field(default=5)


engine = create_engine(POSTGRES_URI)
# engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

def fun_long():
    for i in range(10000):
        x = i**i
    return

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Wait started!')
    # fun_long()
    logger.info('Wait Ended!')

    yield 
    # create_db_and_tables()

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)

logger.info('add fastpai')




@app.get("/")
def health():
    return "Ok !"

# add new books
@app.post("/books", response_model=BookBase)
def create_book(book: BookBase, session: SessionDep):
    db_book = BookBase.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# get books
@app.get("/books/", response_model=list[BookBase])
def read_books(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(BookBase).offset(offset).limit(limit)).all()
    return heroes

# get books by id
@app.get("/books/{id}", response_model=BookBase)
def read_book(id: int, session: SessionDep):
    book = session.get(BookBase, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

