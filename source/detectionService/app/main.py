import logging
import sys
import threading
import queue
import os
import time

import cv2
import numpy as np
import paho.mqtt.client as mqtt

from fastapi import FastAPI
from api.videoFeedEndpointsThreads import router as videoRouter2
from service.detection.detectionThread import detection

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

broker=os.getenv('MQTT_BROKER_URL')
port=int(os.getenv('MQTT_BROKER_PORT'))
username = "sysAdmin"
password = "sysAd2024"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Verbindung erfolgreich hergestellt.")
    else:
        logger.info(f"Verbindung fehlgeschlagen. Fehlercode: {rc}")

def on_message(client, userdata, msg):
    # Das Topic identifiziert die Kamera
    camera_id = msg.topic.split('/')[1]  # Extrahiere 'cam1', 'cam2', etc.
    frameBytes = msg.payload  # Die Nachricht dekodieren
    nparr = np.frombuffer(frameBytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    detection(feedEvent,feedQ,trackEvent,trackQ,frame)

    logger.info(f"Nachricht von {camera_id}: {frame}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)

if len(broker)==0 or port==0:
    logger.info("Missing values to connect to Broker")
    sys.exit()

while True:
    try:
        logger.info("Versuche Verbindung zum Broker...")
        client.connect(broker, port, 60)
        client.loop_start()  # Client im Hintergrund laufen lassen
        break  # Wenn die Verbindung erfolgreich ist, Schleife beenden
    except Exception as e:
        logger.debug(f"Verbindungsfehler: {e}. Neuer Versuch in 5 Sekunden...")
        time.sleep(5)

client.subscribe(topic)
