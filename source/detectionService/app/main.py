import logging
import threading
import queue

from fastapi import FastAPI
from api.video_feed_endpoints import router as videoRouter2
from service.detection.detection_thread import detection_thread

app = FastAPI()
feed_event = threading.Event()  # Event zum Starten und Stoppen des Streams
feed_q = queue.Queue()  # Queue für das Feed (Frames)
track_event = threading.Event()  # Event für Tracking (optional)
track_q = queue.Queue()  # Queue für Tracking-Daten (optional)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]  # Ausgabe in die Konsole
)

detection_thread = threading.Thread(target=detection_thread, args=(feed_event, feed_q, track_event, track_q, 0))
detection_thread.daemon = True  # Daemon-Thread, wird beendet, wenn das Hauptprogramm beendet wird
detection_thread.start()
app.include_router(videoRouter2, prefix="/video", tags=["video"])
