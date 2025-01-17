import base64
import logging
from collections import defaultdict

import cv2
from ultralytics import YOLO
import api.apiRestClientDatabase as ApiRestClientDatabase
from entities.detection.detectedObject import DetectedObject
from entities.detection.trackManager import TrackerManager

TOLERANCE = 10
ADD_REMOVE_THRESHOLD = .5 * 30

model = YOLO("./service/detection/best.pt")

logger = logging.getLogger(__name__)

def processFrame(frame,trackers:TrackerManager):
    results = model.track(frame, conf=0.55, imgsz=640, verbose=False)
    annotatedFrame = results[0].plot()

    currentTrackIds = set()
    if results[0].boxes is not None and results[0].boxes.id is not None:
        currentTrackIds = updateObjectTracking(results, trackers)
    handleDisappearedObjects(currentTrackIds,trackers)

    updateDatabase(trackers,len(results[0].names))

    trackers.previousDetectedObjects = trackers.detectedObjects.copy()

    return annotatedFrame

def updateObjectTracking(results, trackers:TrackerManager):  # von Chatgpt mit anpassungen von uns.
    boxes = results[0].boxes.xywh.cpu()
    trackIds = results[0].boxes.id.int().cpu().tolist()
    clsIds = results[0].boxes.cls.int().cpu().tolist()

    currentTrackIds = set()
    for box, trackId, clsId in zip(boxes, trackIds, clsIds):
        x, y, w, h = map(float, box)
        currentTrackIds.add(trackId)

        # Aktualisiere Klassenhistorie
        trackers.clsIdHistory[trackId][clsId] += 1

        # Berechne Entfernung und aktualisiere Verweilzeit
        if trackers.trackHistory[trackId]:
            lastX, lastY = trackers.trackHistory[trackId][-1]
            distance = ((x - lastX) ** 2 + (y - lastY) ** 2) ** 0.5
        else:
            distance = float('inf')

        if distance <= TOLERANCE:
            trackers.stayTime[trackId] += 1
        else:
            trackers.stayTime[trackId] = 0

        # Objekt hinzufügen, wenn es stabil bleibt
        if trackers.stayTime[trackId] >= ADD_REMOVE_THRESHOLD:
            position= (x,y,w,h)
            trackers.detectedObjects[trackId]=DetectedObject(trackId,clsId,position)
            trackers.disappearanceTime[trackId] = 0

        # Speichere Positionshistorie
        trackers.trackHistory[trackId].append((x, y))
        if len(trackers.trackHistory[trackId]) > 30:
            trackers.trackHistory[trackId].pop(0)
    return currentTrackIds


def handleDisappearedObjects(currentTrackIds, trackers: TrackerManager):
    toRemove = []

    for _, detectOb in trackers.detectedObjects.items():
        trackId = detectOb.getTrackId()
        if trackId not in currentTrackIds:
            trackers.disappearanceTime[trackId] += 1
            if trackers.disappearanceTime[trackId] >= ADD_REMOVE_THRESHOLD:
                toRemove.append(trackId)
        else:
            trackers.disappearanceTime[trackId] = 0

    for trackId in toRemove:
        del trackers.detectedObjects[trackId]


def updateDatabase(trackers:TrackerManager,amountOfCls,annotatedFrame,results:[]):
    detectedObjects = trackers.detectedObjects.copy()
    previousDetectedObjects = trackers.previousDetectedObjects.copy()
    nowDetectedDict = defaultdict(int)
    prevDetectedDict= defaultdict(int)

    for _,nowDetectedOb in detectedObjects.items():
        if nowDetectedOb.getClsId() is not None:
            nowDetectedDict[nowDetectedOb.getClsId()] +=1
    for _,prevDetectedOb in previousDetectedObjects.items():
        if prevDetectedOb.getClsId() is not None:
            prevDetectedDict[prevDetectedOb.getClsId()] +=1

    if not nowDetectedDict == prevDetectedDict:
        addDiff = []
        delDiff = []

        for index in range(amountOfCls-1):
            if nowDetectedDict[index] is not None and prevDetectedDict[index] is not None:
                if nowDetectedDict[index] > prevDetectedDict[index]:
                    addDiff.extend([index] * (nowDetectedDict[index] - prevDetectedDict[index]))
                if prevDetectedDict[index] > nowDetectedDict[index]:
                    delDiff.extend([index] * (prevDetectedDict[index] - nowDetectedDict[index]))
            if nowDetectedDict[index] is None and prevDetectedDict[index] is not None:
                delDiff.extend([index] * (prevDetectedDict[index] - nowDetectedDict[index]))
            if nowDetectedDict[index] is not None and prevDetectedDict[index] is None:
                addDiff.extend([index] * (nowDetectedDict[index] - prevDetectedDict[index]))

        if len(addDiff)>0 or len(delDiff)>0:
            class_ids = get_necessary_class_ids(trackers)
            segmented_images = {}
            for class_id in class_ids:
                segmented_images[class_id] = select_class_frames(class_id, results.copy())
            if len(addDiff)>0:
                ApiRestClientDatabase.addItemToDatabase(addDiff,annotatedFrame,segmented_images)
            if len(delDiff)>0:
                ApiRestClientDatabase.deleteItemFromDatabase(delDiff,annotatedFrame,segmented_images)


def get_necessary_class_ids(trackers:TrackerManager):
    detectedObjects = trackers.detectedObjects.copy()
    necessary_Class_Ids = []
    for _,nowDetectedOb in detectedObjects.items():
        if nowDetectedOb.getClsId() is not None and nowDetectedOb.getClsId() not in necessary_Class_Ids:
            necessary_Class_Ids += [nowDetectedOb.getClsId()]
    return necessary_Class_Ids

def select_class_frames(class_id,results:[]):
    filteredBoxes = results[0].boxes[results[0].boxes.cls == class_id]
    results[0].boxes = filteredBoxes
    annotated_frame = results[0].plot()
    success, buffer = cv2.imencode('.webp', annotated_frame, [cv2.IMWRITE_WEBP_QUALITY, 90])

    if success:
        # Convert the JPEG buffer to Base64
        base64_encoded_image = base64.b64encode(buffer).decode('utf-8')
        # Print or use the Base64 string
        return base64_encoded_image
    else:
        return None