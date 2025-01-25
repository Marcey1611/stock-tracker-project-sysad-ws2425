import paho.mqtt.client as mqtt
import os
import logging
import sys
import uuid
import time
from camera.camera import frame_loop

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]  # Ausgabe in die Konsole
)

logger = logging.getLogger(__name__)

custom_uuid = uuid.uuid4()
broker=os.getenv('MQTT_BROKER_URL')
port=int(os.getenv('MQTT_BROKER_PORT'))
username = "sysAdmin"
password = "sysAd2024"
topic ="camera/"+custom_uuid.__str__()+"/image"
logging.debug(f"Broker {broker} // Port {port}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Verbindung erfolgreich hergestellt.")

    else:
        logger.debug(f"Verbindung fehlgeschlagen. Fehlercode: {rc}")

if len(broker)==0 or port==0:
    logging.info("Missing values to connect to Broker")
    sys.exit()

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(username, password)
while True:
    try:
        logger.info("Versuche Verbindung zum Broker...")
        client.connect(broker, port, 60)
        client.loop_start()  # Client im Hintergrund laufen lassen
        break  # Wenn die Verbindung erfolgreich ist, Schleife beenden
    except Exception as e:
        logger.debug(f"Verbindungsfehler: {e}. Neuer Versuch in 5 Sekunden...")
        time.sleep(5)

frame_loop(client,topic)