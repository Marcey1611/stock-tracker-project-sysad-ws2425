import logging
import threading
from multiprocessing import Process, Queue

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.video_feed_endpoints import router as videoRouter2
from service.detection.detection_thread import detection
from service.http_request.response_thread import response_thread
from service.mqtt.mqtt_client import mqtt_thread

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]  # Ausgabe in die Konsole
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaubt Anfragen von allen Ursprüngen (vorsichtig)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
feed_q = Queue(maxsize=1)  # Queue für das Feed (Frames)
track_q = Queue(maxsize=1)  # Queue für Tracking-Daten (optional)
image_q = Queue()
response_q = Queue(maxsize=1)


topic ="camera/+/image"
app.include_router(videoRouter2, prefix="/video", tags=["video"])

detection_process = Process(target=detection, args=(feed_q,track_q,image_q,response_q))
detection_process.start()

thread_mqtt=threading.Thread(target=mqtt_thread,args=(image_q,))
thread_mqtt.daemon = True
thread_mqtt.start()

thread_response=threading.Thread(target=response_thread,args=(response_q,))
thread_response.daemon = True
thread_response.start()



