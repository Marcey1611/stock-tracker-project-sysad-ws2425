import logging
import threading
import queue
import os

from fastapi import FastAPI
from api.videoFeedEndpointsThreads import router as videoRouter2
from service.detection.detectionThread import detectionThread

app = FastAPI()
feedEvent = threading.Event()  # Event zum Starten und Stoppen des Streams
feedQ = queue.Queue()  # Queue für das Feed (Frames)
trackEvent = threading.Event()  # Event für Tracking (optional)
trackQ = queue.Queue()  # Queue für Tracking-Daten (optional)
addQ = queue.Queue()  # Queue für Tracking-Daten (optional)
removeQ = queue.Queue()  # Queue für Tracking-Daten (optional)



logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]  # Ausgabe in die Konsole
)
cam_url=os.getenv('CAM_SERVICE_URL')
detection_thread = threading.Thread(target=detectionThread, args=(feedEvent, feedQ, trackEvent, trackQ, cam_url))
detection_thread.daemon = True  # Daemon-Thread, wird beendet, wenn das Hauptprogramm beendet wird
detection_thread.start()
app.include_router(videoRouter2, prefix="/thread", tags=["video"])
