from sqlmodel import Field, Session, SQLModel, create_engine, select
import os
import time
import dotenv
from typing import Annotated
from fastapi import Depends
import logging
import requests
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

import asyncio
import asyncpg

# dotenv.load_dotenv('/root/GenAI-BookSummary/my-app/.env')
# POSTGRES_URI = os.getenv('POSTGRES_URI')

POSTGRES_URI='postgresql+asyncpg://postgres:postgres@localhost:5438/postgres'

# engine = create_engine(POSTGRES_URI)
# # engine = create_engine(sqlite_url, connect_args=connect_args)
# def get_session():
#     with Session(engine) as session:
#         logger.info('session')
#         logger.info(session)
#         yield session



async_engine = create_async_engine(
   POSTGRES_URI,
   echo=True,
   future=True
)


async def get_session() -> AsyncSession:
   async_session = sessionmaker(
       bind=async_engine, class_=AsyncSession, expire_on_commit=False
   )
   async with async_session() as session:
       yield session

def check_ollama_model():
    res = requests.get('http://localhost:11434/api/tags')
    if(len(res.json()["models"]) == 0):
        time.sleep(5)
        logger.info('wait while model is loading ...')
        return check_ollama_model()
    else:
        return
      

SessionDep = Annotated[Session, Depends(get_session)]

logger = logging.getLogger('uvicorn.error')
logger.warning("logger start")
logger.warning(SessionDep)

