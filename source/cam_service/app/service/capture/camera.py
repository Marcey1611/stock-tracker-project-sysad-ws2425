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


def frame_loop():
    from service.mqtt.mqtt_client import is_client_connected, publish_image

    camera = cv2.VideoCapture(0,cv2.CAP_V4L2)
    if camera.isOpened():
        logger.info(f"Camera {0} opend.")
    else:
        logger.error(f"Could not open camera:{0}.")
        return  # Beende den Thread, wenn die Kamera nicht geöffnet werden kann
    init_cam(camera)

    while is_client_connected():
        success, frame = capture_image(camera)
        if success:
            _, buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_WEBP_QUALITY, 80])
            publish_image(buffer.tobytes())
        else:
            break


def init_cam(camera:cv2.VideoCapture):
    set_resolution(camera)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    camera.set(cv2.CAP_PROP_FPS,10)
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

def capture_image(camera:cv2.VideoCapture):

    success, frame = camera.read()
    if not success:
        logger.error("Fehler: Kamera liefert kein Bild")
        return False, None
    return True, frame
