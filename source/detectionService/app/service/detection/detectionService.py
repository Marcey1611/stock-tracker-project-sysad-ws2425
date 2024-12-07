import cv2
from ultralytics import YOLO

from camera.cam import camera
from service.apiClientDatabaseService import manageAddToDatabase, manageDeleteToDatabase
from entities.models.detectionModels import  TrackerManager

# Load the YOLO11 model
model = YOLO("./service/detection/best.pt")

def processFrame(frame):
    results = model.track(frame, conf=0.4, persist=True, verbose=False, imgsz=640)
    annotatedFrame = results[0].plot()
    return results, annotatedFrame

def updateObjectTracking(results, trackers, TOLERANCE, ADD_THRESHOLD):
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
        if trackers.stayTime[trackId] >= ADD_THRESHOLD:
            trackers.detectedObjects.add(trackId)
            trackers.disappearanceTime[trackId] = 0

        # Speichere Positionshistorie
        trackers.trackHistory[trackId].append((x, y))
        if len(trackers.trackHistory[trackId]) > 30:
            trackers.trackHistory[trackId].pop(0)
    return currentTrackIds

def handleDisappearedObjects(currentTrackIds, trackers, REMOVE_THRESHOLD):
    for trackId in trackers.detectedObjects.copy():
        if trackId not in currentTrackIds:
            trackers.disappearanceTime[trackId] += 1
            if trackers.disappearanceTime[trackId] >= REMOVE_THRESHOLD:
                trackers.detectedObjects.remove(trackId)
        else:
            trackers.disappearanceTime[trackId] = 0

def updateDatabase(addedObjects, removedObjects, trackers):
    for addedObject in addedObjects:
        if trackers.clsIdHistory[addedObject]:
            mostFrequentClsId = max(
                trackers.clsIdHistory[addedObject],
                key=trackers.clsIdHistory[addedObject].get
            )
            manageAddToDatabase(trackers.restModels, addedObject, mostFrequentClsId)

    for removedObject in removedObjects:
        manageDeleteToDatabase(trackers.restModels, removedObject)

def yoloDetection():
    TOLERANCE = 10
    ADD_THRESHOLD = .5 * 30
    REMOVE_THRESHOLD = .5 * 30

    trackers = TrackerManager()

    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            break

        results, annotatedFrame = processFrame(frame)

        currentTrackIds = set()  # Leere Menge, falls keine Objekte erkannt werden
        if results[0].boxes is not None and results[0].boxes.id is not None:
            currentTrackIds = updateObjectTracking(results, trackers, TOLERANCE, ADD_THRESHOLD)

        handleDisappearedObjects(currentTrackIds, trackers, REMOVE_THRESHOLD)

        # Berechne hinzugefügte und entfernte Objekte
        addedObjects = trackers.detectedObjects - trackers.previousDetectedObjects
        removedObjects = trackers.previousDetectedObjects - trackers.detectedObjects
        updateDatabase(addedObjects, removedObjects, trackers)

        # Aktualisiere vorherige Objekte
        trackers.previousDetectedObjects = trackers.detectedObjects.copy()

        # Frame kodieren und zurückgeben
        ret, buffer = cv2.imencode('.jpg', annotatedFrame)
        if not ret:
            break

        frameBytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frameBytes + b'\r\n\r\n')

    camera.release()
    cv2.destroyAllWindows()