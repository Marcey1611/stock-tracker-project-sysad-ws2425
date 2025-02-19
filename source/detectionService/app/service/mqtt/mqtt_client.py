import os
import logging
import time

import cv2
import numpy as np
import paho.mqtt.client as mqtt
import sys

from service.detection.frame_Codings import decode_frame
from service.http_request.http_request_service import init_database

logger = logging.getLogger(__name__)


broker=os.getenv('MQTT_BROKER_URL')
port=int(os.getenv('MQTT_BROKER_PORT'))
username = "sysAdmin"
password = "sysAd2024"
topic ="camera/+/image"
mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Verbindung erfolgreich hergestellt.")
    else:
        logger.info(f"Verbindung fehlgeschlagen. Fehlercode: {rc}")

def on_disconnect(client, userdata, rc):
    if rc == 0:
        logger.info("Verbindung erfolgreich getrennt.")
    else:
        logger.error(f"Verbindung wurde mit Fehlercode {rc} getrennt.")


def on_message(client, userdata, msg):
    image_q,count = userdata
    camera_id = msg.topic.split('/')[1]
    frame_bytes = msg.payload
    if count == 0:
        frame = decode_frame(msg.payload)
        init_database(frame)
    image_q.put_nowait(frame_bytes)
    count = count + 1
    logger.debug(f"Nachricht von {camera_id}")
    client.user_data_set((image_q,count))

def mqtt_thread(image_q):
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect
    count = 0
    mqtt_client.user_data_set((image_q,count))
    mqtt_client.username_pw_set(username, password)

    if len(broker)==0 or port==0:
        logger.info("Missing values to connect to Broker")
        sys.exit()
    while True:
        try:
            logger.info("Versuche Verbindung zum Broker...")
            mqtt_client.connect(broker, port, 60)
            mqtt_client.loop_start()  # Client im Hintergrund laufen lassen
            break  # Wenn die Verbindung erfolgreich ist, Schleife beenden
        except Exception as e:
            logger.debug(f"Verbindungsfehler: {e}. Neuer Versuch in 5 Sekunden...")
            time.sleep(5)

    mqtt_client.subscribe(topic)