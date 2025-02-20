import os
import sys
import uuid
import logging
import time
import paho.mqtt.client as mqtt

from service.capture.camera import frame_loop

logger = logging.getLogger(__name__)

custom_uuid = uuid.uuid4()
broker=os.getenv('MQTT_BROKER_URL')
port=int(os.getenv('MQTT_BROKER_PORT'))
username = os.getenv('MQTT_USERNAME')
password =os.getenv('MQTT_PASSWORD')
topic ="camera/"+custom_uuid.__str__()+"/image"
logger.debug(f"Broker {broker} // Port {port}")

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Verbindung erfolgreich hergestellt.")

    else:
        logger.debug(f"Verbindung fehlgeschlagen. Fehlercode: {rc}")

def on_disconnect(client, userdata, flags):
    logger.info("Disconnected From MQTT Broker")

def init_mqtt_client():
    if len(broker) == 0 or port == 0:
        logging.info("Missing values to connect to Broker")
        sys.exit()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    if username is not None and password is not None:
        client.username_pw_set(username, password)

def try_connecting():
    try:
        logger.info("Versuche Verbindung zum Broker...")
        client.connect(broker, port, 60)
        client.loop_start()  # Client im Hintergrund laufen lassen
        return True # Wenn die Verbindung erfolgreich ist, Schleife beenden
    except Exception as e:
        logger.debug(f"Verbindungsfehler: {e}. Neuer Versuch in 10 Sekunden...")
        time.sleep(10)
        return False

def is_client_connected():
    return client.is_connected()

def publish_image(frame_bytes):
    logger.debug(f"length : {len(frame_bytes)}")
    client.publish(topic, payload=frame_bytes)
    logger.debug(f"Published frame at: {time.monotonic()}")  # Zeit loggen