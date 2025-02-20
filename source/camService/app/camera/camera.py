import logging
import time

import paho.mqtt.client as mqtt
import cv2

logger = logging.getLogger(__name__)

resolutions = [
    (3840, 2160),  # 4K
    (2560, 1440),  # QHD
    (1920, 1080),  # Full HD
    (1280, 720),   # HD
    (640, 480)     # SD
]

frame_interval = 0.33  # 2 FPS = 1 Frame alle 0.5 Sekunden

def frame_loop(client:mqtt.Client,topic:str):
    last_frame_time = time.monotonic()

    camera = cv2.VideoCapture(0)
    if camera.isOpened():
        logger.info(f"Camera {0} opend.")
    else:
        logger.error(f"Could not open camera:{0}.")
        return  # Beende den Thread, wenn die Kamera nicht geöffnet werden kann
    init_cam(camera)

    while client.is_connected():
        current_time = time.monotonic()
        elapsed_time = current_time - last_frame_time

        if elapsed_time < frame_interval:
            time.sleep(frame_interval - elapsed_time)  # Wartezeit einfügen

        last_frame_time = time.monotonic()  # Zeit aktualisieren

        success, frame = camera.read()
        if not success:
            logger.error("Fehler: Kamera liefert kein Bild")
            break

        _, buffer = cv2.imencode('.webp', frame, [cv2.IMWRITE_WEBP_QUALITY, 80])
        frameBytes = buffer.tobytes()
        logger.debug(f"length : {len(frameBytes)}")
        client.publish(topic, payload=frameBytes)
        logger.debug(f"Published frame at: {time.monotonic()}")  # Zeit loggen


def init_cam(camera:cv2.VideoCapture):
    desired_fps = 5
    set_resolution(camera)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))
    camera.set(cv2.CAP_PROP_FPS, desired_fps)
    actual_fps = camera.get(cv2.CAP_PROP_FPS)
    logger.debug(f"Kamera-FPS: {actual_fps}")


def set_resolution(camera:cv2.VideoCapture):
    for width, height in resolutions:
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Prüfen, ob die Kamera die Auflösung akzeptiert
        actual_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if actual_width == width and actual_height == height:
            print(f"Camera resolution: {actual_width}x{actual_height}")
            break
