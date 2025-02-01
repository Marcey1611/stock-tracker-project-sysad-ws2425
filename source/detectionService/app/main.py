import logging
import sys
import threading
import queue
import time

import cv2
import numpy as np
import paho.mqtt.client as mqtt

from fastapi import FastAPI
from api.videoFeedEndpointsThreads import router as videoRouter2
from service.detection.detectionThread import detection
from service.mqtt.mqtt_client import mqtt_thread

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]  # Ausgabe in die Konsole
)

logger = logging.getLogger(__name__)

app = FastAPI()
feedEvent = threading.Event()  # Event zum Starten und Stoppen des Streams
feedQ = queue.Queue()  # Queue für das Feed (Frames)
trackEvent = threading.Event()  # Event für Tracking (optional)
trackQ = queue.Queue()  # Queue für Tracking-Daten (optional)
addQ = queue.Queue()  # Queue für Tracking-Daten (optional)
removeQ = queue.Queue()  # Queue für Tracking-Daten (optional)


topic ="camera/+/image"
app.include_router(videoRouter2, prefix="/thread", tags=["video"])

thread_mqtt=threading.Thread(target=mqtt_thread,args=(feedEvent,feedQ,trackEvent,trackQ))
thread_mqtt.daemon = True
thread_mqtt.start()



