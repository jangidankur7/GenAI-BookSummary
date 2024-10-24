from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

class BookBase(SQLModel, table=True):
    __tablename__ = "books"
    id: int  | None = Field(index=True, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    genre: str = Field(index=True)
    year_published: datetime = Field(index=True)
    summary: str | None = Field(default=None, index=True)

class BookUpdate(SQLModel):
    title: str | None = None
    author: str | None = None
    genre: int | None = None
    year_published: datetime | None = None 
    summary: str | None = None


