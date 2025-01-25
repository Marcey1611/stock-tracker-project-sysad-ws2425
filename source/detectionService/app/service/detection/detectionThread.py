import logging
import queue
from threading import Event
import cv2
import api.apiRestClientDatabase as ApiRestClientDatabase
from entities.detection.trackManager import TrackerManager

from service.detection.frameProccess import processFrame
from service.detection.humanCheck import isHumanInFrame

logger = logging.getLogger('detection')


def detection(feedEvent:Event,feedQ:queue.Queue,trackEvent:Event,trackQ:queue.Queue,frame):
    ApiRestClientDatabase.clearAll()

    trackers = TrackerManager()

    humanCheck, annotatedFrame = isHumanInFrame(frame)
    if humanCheck:
        if feedEvent.is_set():
            streamFeedFrames(frame, feedQ)
        if trackEvent.is_set():
            streamFeedFrames(annotatedFrame, trackQ)

    else:
        annotatedFrame = processFrame(frame,trackers)

        if feedEvent.is_set():
            streamFeedFrames(frame, feedQ)
        if trackEvent.is_set():
            streamFeedFrames(annotatedFrame, trackQ)


def streamFeedFrames(frame,feedQ:queue.Queue):
    _, buffer = cv2.imencode('.webp', frame)
    frameBytes = buffer.tobytes()
    feedQ.put(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frameBytes + b'\r\n')


