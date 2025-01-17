import logging
import queue
from threading import Event
import cv2
import api.apiRestClientDatabase as ApiRestClientDatabase
from entities.detection.trackManager import TrackerManager

from service.detection.frameProccess import processFrame
from service.detection.humanCheck import isHumanInFrame

logger = logging.getLogger('detectionThread')


def detectionThread(feedEvent:Event,feedQ:queue.Queue,trackEvent:Event,trackQ:queue.Queue,source):
    ApiRestClientDatabase.clearAll()
    camera = cv2.VideoCapture(source)
    if camera.isOpened():
        logger.info(f"Camera {source} opend.")
    else:
        logger.error(f"Could not open camera:{source}.")
        return  # Beende den Thread, wenn die Kamera nicht geöffnet werden kann
    initCam(camera,source)

    trackers = TrackerManager()

    while True:
        success, frame = camera.read()  # Frame von der Kamera lesen
        if not success:
            logger.error("Error could not access camera frame.")
            break
        else:
            humanCheck, annotatedFrame = isHumanInFrame(frame)
            if humanCheck:
                if feedEvent.is_set():
                    streamFrames(frame, feedQ)
                if trackEvent.is_set():
                    if not streamFrames(annotatedFrame, trackQ):
                        break
            else:
                annotatedFrame = processFrame(frame,trackers)

                if feedEvent.is_set():
                    streamFrames(frame, feedQ)
                if trackEvent.is_set():
                    if not streamFrames(annotatedFrame, trackQ):
                        break

    camera.release()
    logger.info(f"Camera {source} closed.")

def streamFrames(frame,feedQ:queue.Queue):
    ret, buffer = cv2.imencode('.webp', frame)
    if not ret:
        return False
    frameBytes = buffer.tobytes()
    logger.debug(frameBytes)
    feedQ.put(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frameBytes + b'\r\n')
    return True

def initCam(camera:cv2.VideoCapture,source):
    desiredWidth = 1920
    desiredHeight = 1080

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, desiredWidth)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, desiredHeight)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    frameWidth = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    frameHeight = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    logger.debug(f"Camera resolution:{str(source)}: {int(frameWidth)}x{int(frameHeight)}")