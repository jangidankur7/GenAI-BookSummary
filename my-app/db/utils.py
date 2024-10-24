from sqlmodel import Field, Session, SQLModel, create_engine, select
import os
import dotenv
from typing import Annotated
from fastapi import Depends
import logging

# dotenv.load_dotenv('/root/GenAI-BookSummary/my-app/.env')
# POSTGRES_URI = os.getenv('POSTGRES_URI')

POSTGRES_URI='postgresql://avnadmin:AVNS_IzoUvCF2an6Q-ro89o6@postgres-aiven-officialaviid-2c3c.i.aivencloud.com:17942/defaultdb?sslmode=require'

engine = create_engine(POSTGRES_URI)
# engine = create_engine(sqlite_url, connect_args=connect_args)
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
logger = logging.getLogger('uvicorn.error')