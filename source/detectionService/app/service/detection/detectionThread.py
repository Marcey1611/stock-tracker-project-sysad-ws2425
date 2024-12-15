import logging
import queue
from threading import Event
from ultralytics import YOLO
import cv2
import time
import api.apiRestClientDatabase

logger = logging.getLogger('detectionThread')

model = YOLO("./service/detection/yolo11x.pt")

def detectionThread(feedEvent:Event,feedQ:queue.Queue,trackEvent:Event,trackQ:queue.Queue,source):
    try:
        api.apiRestClientDatabase.clearAll()
        camera = cv2.VideoCapture(source)
        if camera.isOpened():
            logger.info(f"Kamera {source} wurde geöffnet.")
        else:
            logger.debug(f"Fehler: Kamera {source} konnte nicht geöffnet werden.")
            return  # Beende den Thread, wenn die Kamera nicht geöffnet werden kann
        initCam(camera,source)

        while True:
            success, frame = camera.read()  # Frame von der Kamera lesen
            if not success:
                logger.debug("Fehler beim Abrufen des Frames von der Kamera.")
                break
            else:
                success, frame = camera.read()
                if not success:
                    break

                annotatedFrame = processFrame(frame)


                if feedEvent.is_set():
                    _, buffer = cv2.imencode('.jpg', frame)
                    frameBytes = buffer.tobytes()
                    feedQ.put(b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frameBytes + b'\r\n')
                if trackEvent.is_set():
                    # Frame kodieren und zurückgeben
                    ret, buffer = cv2.imencode('.jpg', annotatedFrame)
                    if not ret:
                        break

                    frameBytes = buffer.tobytes()
                    trackQ.put(b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frameBytes + b'\r\n')

        camera.release()
        logger.info(f"Kamera {source} wurde geschlossen.")
    except cv2.error as e:
        logger.error(f"OpenCV-Fehler: {e}")



objectCountHistory = {}  # Historie der erkannten Objekte pro Klasse
objectTimestamps = {}  # Zeitstempel für das erste Auftreten jeder Klasse
removalTimestamps = {}  # Zeitstempel für das letzte Verschwinden jeder Klasse
DELAY = 2  # Verzögerung in Sekunden, bevor ein Objekt als hinzugefügt/entfernt gilt

def processFrame(frame):
    results = model.predict(frame, conf=0.55, imgsz=640, verbose=False)
    annotatedFrame = results[0].plot()
    detected_objects = results[0].boxes.cls.int().cpu().tolist()
    currentClasses = set(detected_objects)

    addedClasses = []
    removedClasses = []

    # Initialisiere die Historie beim ersten Aufruf
    global objectCountHistory, objectTimestamps, removalTimestamps
    current_time = time.time()

    if not objectCountHistory:
        objectCountHistory = {cls: True for cls in currentClasses}
        objectTimestamps = {cls: current_time for cls in currentClasses}
        addedClasses = list(currentClasses)
        updateDatabase(addedClasses, removedClasses)
        return annotatedFrame

    # Überprüfe hinzugefügte Klassen
    for cls in currentClasses:
        if cls not in objectCountHistory:
            if cls not in objectTimestamps:
                objectTimestamps[cls] = current_time  # Speichere den Zeitstempel
            elif current_time - objectTimestamps[cls] >= DELAY:
                addedClasses.append(cls)
                objectCountHistory[cls] = True
                del objectTimestamps[cls]  # Entferne den Zeitstempel, da die Klasse nun hinzugefügt wurde

    # Überprüfe entfernte Klassen
    for cls in list(objectCountHistory.keys()):
        if cls not in currentClasses:
            if cls not in removalTimestamps:
                removalTimestamps[cls] = current_time  # Speichere den Zeitstempel
            elif current_time - removalTimestamps[cls] >= DELAY:
                removedClasses.append(cls)
                del objectCountHistory[cls]
                del removalTimestamps[cls]  # Entferne den Zeitstempel, da die Klasse nun entfernt wurde

    # Aktualisiere Zeitstempel für erkannte Objekte
    for cls in list(objectTimestamps.keys()):
        if cls not in currentClasses:
            del objectTimestamps[cls]  # Entferne Zeitstempel, wenn die Klasse nicht mehr erkannt wird

    for cls in list(removalTimestamps.keys()):
        if cls in currentClasses:
            del removalTimestamps[cls]  # Entferne den Entfernungstempel, wenn die Klasse wieder erkannt wird

    updateDatabase(addedClasses, removedClasses)
    return annotatedFrame


def updateDatabase(addedObjects, removedObjects):
    if len(addedObjects):
        addArray=[]
        for addedObject in addedObjects:
            logger.info(f"debug {addedObject}")
            addArray.append(addedObjects)
        api.apiRestClientDatabase.addItemToDatabase(addArray)

    if len(removedObjects)>0:
        removeArray = []
        for removedObject in removedObjects:
            logger.debug(f"removed {removedObject}")
            removeArray.append(removedObject)
        api.apiRestClientDatabase.deleteItemFromDatabase(removeArray)

def initCam(camera:cv2.VideoCapture,source):
    desiredWidth = 1920
    desiredHeight = 1080

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, desiredWidth)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, desiredHeight)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    frameWidth = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    frameHeight = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    logger.debug(f"Auflösung der Kamera{str(source)}: {int(frameWidth)}x{int(frameHeight)}")