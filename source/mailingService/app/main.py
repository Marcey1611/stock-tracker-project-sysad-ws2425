from fastapi import FastAPI 
from api.boundary import api
from api.boundary import exception_handler
import logging

logging.basicConfig(
    level=logging.INFO,
    format='MailingService: %(levelname)s - %(asctime)s - %(filename)s - %(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

app = FastAPI()
exception_handler.register_exception_handlers(app)
app.include_router(api.api_router)