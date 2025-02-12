import logging
import threading
import queue

from fastapi import FastAPI
from api.video_feed_endpoints import router as videoRouter2
from service.mqtt.mqtt_client import mqtt_thread

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]  # Ausgabe in die Konsole
)

logger = logging.getLogger(__name__)

app = FastAPI()
feed_event = threading.Event()  # Event zum Starten und Stoppen des Streams
feed_q = queue.Queue()  # Queue für das Feed (Frames)
track_event = threading.Event()  # Event für Tracking (optional)
track_q = queue.Queue()  # Queue für Tracking-Daten (optional)


topic ="camera/+/image"
app.include_router(videoRouter2, prefix="/video", tags=["video"])

thread_mqtt=threading.Thread(target=mqtt_thread,args=(feed_event,feed_q,track_event,track_q))
thread_mqtt.daemon = True
thread_mqtt.start()



