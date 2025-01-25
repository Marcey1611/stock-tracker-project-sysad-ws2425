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

def frame_loop(client:mqtt.Client,topic:str):

    camera = cv2.VideoCapture(0)
    if camera.isOpened():
        logger.info(f"Camera {0} opend.")
    else:
        logger.error(f"Could not open camera:{0}.")
        return  # Beende den Thread, wenn die Kamera nicht geöffnet werden kann
    init_cam(camera)

    while True:
        success, frame = camera.read()  # Frame von der Kamera lesen
        if not success:
            logger.error("Error could not access camera frame.")
            break
        else:
            _, buffer = cv2.imencode('.webp', frame)
            frameBytes = buffer.tobytes()
            client.publish(topic,payload=frameBytes)
            logger.debug(f"Published frame at: {time.time()}")


def init_cam(camera:cv2.VideoCapture):
    desired_fps = 2
    set_resolution(camera)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))
    camera.set(cv2.CAP_PROP_FPS, desired_fps)


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
