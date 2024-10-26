from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from db.utils import logger, check_ollama_model
# import add_router

from api import books

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Loading ollama model !!!')
    check_ollama_model()
    logger.info('model loaded ...')
    

    yield 
    # create_db_and_tables()

app = FastAPI(lifespan=lifespan)
app.include_router(books.router)

logger.info('add fastpai')

@app.get("/")
def health():
    return "Ok !"
