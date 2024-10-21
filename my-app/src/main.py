from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from db.utils import logger
# import add_router

from api import books

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Wait started!')
    # fun_long()
    logger.info('Wait Ended!')

    yield 
    # create_db_and_tables()

app = FastAPI(lifespan=lifespan)
app.include_router(books.router)

logger.info('add fastpai')

@app.get("/")
def health():
    return "Ok !"
