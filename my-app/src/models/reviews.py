from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

class ReviewBase(SQLModel, table=True):
    __tablename__ = "reviews"
    id: int| None = Field(index=True, primary_key=True)
    book_id: int = Field(index=True, foreign_key="books.id")
    user_id: int | None = Field(default=None)
    review_text : str | None = Field(default=None)
    review_text : int = Field(default=5)
