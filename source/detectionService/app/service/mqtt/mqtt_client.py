import os
import logging
import time

import cv2
import numpy as np
import paho.mqtt.client as mqtt
import sys

from entities.detection.track_manager import TrackerManager
from service.detection.detection_thread import detection
from service.http_request.http_request_service import init_database

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
    feed_q, track_q, trackers,count,model_cls_names = userdata
    camera_id = msg.topic.split('/')[1]
    frame_bytes = msg.payload
    np_arr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if count == 0:
        init_database(frame,model_cls_names)
    detection(feed_q,track_q,frame,frame_bytes,trackers)
    count = count + 1
    logger.debug(f"Nachricht von {camera_id}")
    client.user_data_set((feed_q, track_q,trackers,count,model_cls_names))

def mqtt_thread(feed_q,track_q):
    from service.detection.frame_processess import model_cls_names
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    trackers = TrackerManager()
    count = 0
    client.user_data_set(( feed_q, track_q,trackers,count,model_cls_names))
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