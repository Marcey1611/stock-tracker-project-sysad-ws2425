import logging

from fastapi import FastAPI
from routesVideo import router as video_router

app = FastAPI()
app.include_router(video_router, prefix="/video", tags=["video"])

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]  # Ausgabe in die Konsole
)
