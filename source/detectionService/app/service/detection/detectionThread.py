import logging
import queue
from threading import Event
import cv2
from entities.detection.trackManager import TrackerManager

from service.detection.frameProccess import processFrame
from service.detection.humanCheck import isHumanInFrame

logger = logging.getLogger('detection')


def detection(feedEvent:Event,feedQ:queue.Queue,trackEvent:Event,trackQ:queue.Queue,frame,frameBytes,count):
    trackers = TrackerManager()

    humanCheck, annotatedFrame = isHumanInFrame(frame)
    if humanCheck:
        if feedEvent.is_set():
            streamFeedFrames(frame, frameBytes,feedQ)
        if trackEvent.is_set():
            streamFeedFrames(annotatedFrame, None,trackQ)

    else:
        annotatedFrame = processFrame(frame,trackers,count)

        if feedEvent.is_set():
            streamFeedFrames(frame, frameBytes,feedQ)
        if trackEvent.is_set():
            streamFeedFrames(annotatedFrame,None ,trackQ)


def streamFeedFrames(frame,frameBytes,feedQ:queue.Queue):
    if frameBytes is None:
        _, buffer = cv2.imencode('.webp', frame)
        frameBytes = buffer.tobytes()

    feedQ.put_nowait(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frameBytes + b'\r\n')