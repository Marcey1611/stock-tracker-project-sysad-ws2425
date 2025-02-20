import logging
import threading
from multiprocessing import Queue

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.video_feed_endpoints import router as videoRouter2
from service.mqtt.mqtt_client import mqtt_thread

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(videoRouter2, prefix="/video", tags=["video"])

# Queues are there to enable the communication between the two threads
feed_q = Queue(maxsize=1)
track_q = Queue(maxsize=1)
#thread to separate the detection and everything else.
thread_mqtt=threading.Thread(target=mqtt_thread,args=(feed_q,track_q))
thread_mqtt.daemon = True
thread_mqtt.start()



