import os
import logging
import time

import cv2
import numpy as np
import paho.mqtt.client as mqtt
import sys

from service.detection.detectionThread import detection

logger = logging.getLogger(__name__)


broker=os.getenv('MQTT_BROKER_URL')
port=int(os.getenv('MQTT_BROKER_PORT'))
username = "sysAdmin"
password = "sysAd2024"
topic ="camera/+/image"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Verbindung erfolgreich hergestellt.")
    else:
        logger.info(f"Verbindung fehlgeschlagen. Fehlercode: {rc}")

def on_message(client, userdata, msg):
    # Das Topic identifiziert die Kamera
    feedEvent, feedQ, trackEvent, trackQ,count = userdata

    camera_id = msg.topic.split('/')[1]  # Extrahiere 'cam1', 'cam2', etc.
    frameBytes = msg.payload  # Die Nachricht dekodieren
    nparr = np.frombuffer(frameBytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    detection(feedEvent,feedQ,trackEvent,trackQ,frame,frameBytes,count)
    count = count +1

    logger.info(f"Nachricht von {camera_id}")

def mqtt_thread(feedEvent,feedQ,trackEvent,trackQ):
    count = 0
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.user_data_set((feedEvent, feedQ, trackEvent, trackQ,count))
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