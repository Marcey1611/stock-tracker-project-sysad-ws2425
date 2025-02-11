#Entrypoint
import logging
from fastapi import FastAPI 
from api.boundary import api

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(filename)s - %(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

app = FastAPI()
app.include_router(api.router)