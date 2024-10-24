from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

class ReviewBase(SQLModel, table=True):
    __tablename__ = "reviews"
    id: int | None = Field(index=True, primary_key=True)
    book_id: int | None = Field(index=True, foreign_key="books.id")
    user_id: int = Field(default=2)
    review_text : str  = Field(default="below average")
    rating : int = Field(default=2)
    created_at: datetime = Field(index=True)
