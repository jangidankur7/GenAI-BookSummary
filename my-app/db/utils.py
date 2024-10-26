from sqlmodel import Field, Session, SQLModel, create_engine, select
import os
import time
import dotenv
from typing import Annotated
from fastapi import Depends
import logging
import requests

import asyncio
import asyncpg

# dotenv.load_dotenv('/root/GenAI-BookSummary/my-app/.env')
# POSTGRES_URI = os.getenv('POSTGRES_URI')

POSTGRES_URI='postgresql://postgres:postgres@localhost:5438/postgres'

engine = create_engine(POSTGRES_URI)
# engine = create_engine(sqlite_url, connect_args=connect_args)
def get_session():
    with Session(engine) as session:
        logger.info('session')
        logger.info(session)
        yield session


def check_ollama_model():
    res = requests.get('http://localhost:11434/api/tags')
    if(len(res.json()["models"]) == 0):
        time.sleep(5)
        logger.info('wait while model is loading ...')
        return check_ollama_model()
    else:
        return
      
def check_postgres_db():
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

