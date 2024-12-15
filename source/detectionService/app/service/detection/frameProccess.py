from ultralytics import YOLO
import time
import api.apiRestClientDatabase as ApiRestClientDatabase

objectCountHistory = {}  # Historie der erkannten Objekte pro Klasse
objectTimestamps = {}  # Zeitstempel für das erste Auftreten jeder Klasse
removalTimestamps = {}  # Zeitstempel für das letzte Verschwinden jeder Klasse
DELAY = 2  # Verzögerung in Sekunden, bevor ein Objekt als hinzugefügt/entfernt gilt


model = YOLO("./service/detection/best.pt")


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

    checkForAddObjects(currentClasses,current_time, addedClasses)

    checkForDelObjects(currentClasses, current_time, removedClasses)

    # Aktualisiere Zeitstempel für erkannte Objekte
    for cls in list(objectTimestamps.keys()):
        if cls not in currentClasses:
            del objectTimestamps[cls]  # Entferne Zeitstempel, wenn die Klasse nicht mehr erkannt wird

    for cls in list(removalTimestamps.keys()):
        if cls in currentClasses:
            del removalTimestamps[cls]  # Entferne den Entfernungstempel, wenn die Klasse wieder erkannt wird

    updateDatabase(addedClasses, removedClasses)
    return annotatedFrame
def checkForAddObjects(currentClasses,current_time,addedClasses):
    # Überprüfe hinzugefügte Klassen
    for cls in currentClasses:
        if cls not in objectCountHistory:
            if cls not in objectTimestamps:
                objectTimestamps[cls] = current_time  # Speichere den Zeitstempel
            elif current_time - objectTimestamps[cls] >= DELAY:
                addedClasses.append(cls)
                objectCountHistory[cls] = True
                del objectTimestamps[cls]  # Entferne den Zeitstempel, da die Klasse nun hinzugefügt wurde

def checkForDelObjects(currentClasses,current_time,removedClasses):
    for cls in list(objectCountHistory.keys()):
        if cls not in currentClasses:
            if cls not in removalTimestamps:
                removalTimestamps[cls] = current_time  # Speichere den Zeitstempel
            elif current_time - removalTimestamps[cls] >= DELAY:
                removedClasses.append(cls)
                del objectCountHistory[cls]
                del removalTimestamps[cls]  # Entferne den Zeitstempel, da die Klasse nun entfernt wurde

def updateDatabase(addedObjects, removedObjects):
    if len(addedObjects):
        addArray=[]
        for addedObject in addedObjects:
            addArray.append(addedObject)
        ApiRestClientDatabase.addItemToDatabase(addArray)

    if len(removedObjects)>0:
        removeArray = []
        for removedObject in removedObjects:
            removeArray.append(removedObject)
        ApiRestClientDatabase.deleteItemFromDatabase(removeArray)