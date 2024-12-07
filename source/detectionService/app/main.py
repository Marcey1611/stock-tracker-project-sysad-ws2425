import logging

from fastapi import FastAPI
from api.videoFeedEndpoints import router as videoRouter

app = FastAPI()
app.include_router(videoRouter, prefix="/video", tags=["video"])

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]  # Ausgabe in die Konsole
)