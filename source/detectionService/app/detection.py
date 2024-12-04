import cv2
from cam import camera
from ultralytics import YOLO
from collections import defaultdict
import numpy as np
from RequestModuls import AddRequest
from RequestModuls import DeleteRequest
from dataService import sendAddToDatabaseService
from dataService import sendDeleteToDatabaseService


# Load the YOLO11 model
model = YOLO("best.pt")

def yolo_detection():
    track_history = defaultdict(lambda: [])
    stay_time = defaultdict(lambda: 0)  # Verweilzeit für jedes Objekt
    detected_objects = set()  # Objekte, die sich im Bild befinden
    previous_detected_objects = set()  # Zustand des vorherigen Frames
    disappearance_time = defaultdict(lambda: 0)  # Zeit, wie lange ein Objekt verschwunden ist
    cls_id_history = defaultdict(lambda: defaultdict(lambda: 0))  # Speichert die cls_id-Häufigkeit pro track_id
    restModels = defaultdict(lambda: AddRequest(-1))

    TOLERANCE = 10  # Positionstoleranz in Pixeln
    ADD_THRESHOLD = 1 * 30  # Delay beim Hinzufügen
    REMOVE_THRESHOLD = 1 * 30  # Delay beim Entfernen

    while camera.isOpened():
        success, frame = camera.read()

        if success:
            annotated_frame = frame.copy()

            results = model.track(frame,conf=0.4,persist=True, verbose=True,imgsz=1088)
            current_track_ids = set()

            # Wenn es erkannte Boxen gibt
            if results[0].boxes is not None and results[0].boxes.id is not None:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()
                cls_ids = results[0].boxes.cls.int().cpu().tolist()  # Klassen-IDs

                annotated_frame = results[0].plot()

                for box, track_id, cls_id in zip(boxes, track_ids, cls_ids):
                    x, y, w, h = box
                    x, y = float(x), float(y)

                    current_track_ids.add(track_id)

                    # Aktualisiere Klassenhistorie
                    cls_id_history[track_id][cls_id] += 1

                    # Berechne Entfernung zur letzten bekannten Position
                    if track_history[track_id]:
                        last_x, last_y = track_history[track_id][-1]
                        distance = ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5
                    else:
                        distance = float('inf')

                    # Aktualisiere Verweilzeit
                    if distance <= TOLERANCE:
                        stay_time[track_id] += 1
                    else:
                        stay_time[track_id] = 0

                    # Wenn Objekt hinzugefügt wird
                    if stay_time[track_id] >= ADD_THRESHOLD:
                        detected_objects.add(track_id)
                        disappearance_time[track_id] = 0

                    # Speichere Positionshistorie
                    track_history[track_id].append((x, y))
                    if len(track_history[track_id]) > 30:
                        track_history[track_id].pop(0)

                    # Zeichne Bewegungsverlauf
                    points = np.hstack(track_history[track_id]).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

            # Prüfe auf verschwundene Objekte
            for track_id in detected_objects.copy():
                if track_id not in current_track_ids:
                    disappearance_time[track_id] += 1
                    if disappearance_time[track_id] >= REMOVE_THRESHOLD:
                        detected_objects.remove(track_id)
                else:
                    disappearance_time[track_id] = 0

            # Hinzugefügte und entfernte Objekte feststellen
            added_objects = detected_objects - previous_detected_objects
            removed_objects = previous_detected_objects - detected_objects
            if added_objects:
                print(f"Neue Objekte hinzugefügt: {added_objects}")
                for added_object in added_objects:
                    if cls_id_history[added_object]:
                        most_frequent_cls_id = max(cls_id_history[added_object], key=cls_id_history[added_object].get)
                        print(f"Objekt {added_object}: Häufigste Klasse bisher: {most_frequent_cls_id}")
                        #reqData = AddRequest(most_frequent_cls_id)
                        #restModels[added_object]=reqData
                        #sendAddToDatabaseService(reqData)

                        #hier bitte die ADD funktion aufrufen und neuer thread und env wenn aleine.

            if removed_objects:
                #reqData = DeleteRequest.fromAddRequest(restModels[removed_objects])
                #del restModels[removed_objects]
                #sendDeleteToDatabaseService(reqData)
                print(f"Objekte entfernt: {removed_objects}")
                #hier bitte die Deletfunktion aurufen.

            previous_detected_objects = detected_objects.copy()

            # Frame kodieren und zurückgeben
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            if not ret:
                break

            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        else:
            break

    camera.release()
    cv2.destroyAllWindows()

