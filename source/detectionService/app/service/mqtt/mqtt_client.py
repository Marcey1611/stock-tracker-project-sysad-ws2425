import os
import logging
import time
import paho.mqtt.client as mqtt
import sys

from entities.detection.track_manager import TrackerManager
from service.detection.frame_handling import frame_handling
from service.detection.frame_codings import decode_frame
from service.http_request.http_request_service import init_database

logger = logging.getLogger(__name__)


broker=os.getenv('MQTT_BROKER_URL')
port=int(os.getenv('MQTT_BROKER_PORT'))
username = os.getenv('MQTT_USERNAME')
password =os.getenv('MQTT_PASSWORD')
topic ="camera/+/image"
client = mqtt.Client()


def on_connect(inner_client, userdata, flags, rc):
    if rc == 0:
        logger.info("Verbindung erfolgreich hergestellt.")
    else:
        logger.info(f"Verbindung fehlgeschlagen. Fehlercode: {rc}")

def on_disconnect(inner_client, userdata, flags):
    logger.info("Disconnected From MQTT Broker")

def on_message(inner_client, userdata, msg):
    feed_q, track_q, trackers,count,model_cls_names = userdata
    camera_id = msg.topic.split('/')[1]
    frame_bytes = msg.payload
    frame = decode_frame(frame_bytes)
    if count == 0:
        init_database(frame,model_cls_names)
    frame_handling(feed_q, track_q, frame, frame_bytes, trackers)
    count = count + 1
    logger.debug(f"Nachricht von {camera_id}")
    inner_client.user_data_set((feed_q, track_q,trackers,count,model_cls_names))

def mqtt_thread(feed_q,track_q):
    from service.detection.frame_detecting import model_cls_names
    init_mqtt_client()
    trackers = TrackerManager()
    count = 0
    client.user_data_set(( feed_q, track_q,trackers,count,model_cls_names))

    connected = False
    while not connected:
        connected = try_connecting()
    client.subscribe(topic)


def init_mqtt_client():
    if len(broker) == 0 or port == 0:
        logging.info("Missing values to connect to Broker")
        sys.exit()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    if username is not None and password is not None:
        client.username_pw_set(username, password)


def try_connecting():
    try:
        logger.info("Versuche Verbindung zum Broker...")
        client.connect(broker, port, 60)
        client.loop_start()
        return True
    except Exception as e:
        logger.debug(f"Verbindungsfehler: {e}. Neuer Versuch in 10 Sekunden...")
        time.sleep(10)
        return False