import logging
from service.mqtt.mqtt_client import init_mqtt_client,try_connecting
from service.capture.camera import frame_loop

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]  # Ausgabe in die Konsole
)

logger = logging.getLogger(__name__)

init_mqtt_client()
logger.info(f"Init MQTT-Client")
while True:
    connected = False
    while not connected:
        connected = try_connecting()
    frame_loop()