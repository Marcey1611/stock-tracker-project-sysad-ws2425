import base64
import copy
import logging
from collections import defaultdict
from typing import Dict

import cv2

from ultralytics import YOLO
import api.api_rest_client_database as api_rest_client_database
import entities.http.database_models as http_database_models
from entities.detection.detected_object import DetectedObject
from entities.detection.track_manager import TrackerManager
from entities.detection.product import Product


TOLERANCE = 10
ADD_REMOVE_THRESHOLD = .5 * 30

model = YOLO("./service/detection/yolo11l.pt")

logger = logging.getLogger(__name__)


def process_frame(frame, trackers: TrackerManager):
    results = model.track(frame, conf=0.55, imgsz=640, verbose=False)
    annotated_frame = results[0].plot()

    current_track_ids = set()
    if results[0].boxes is not None and results[0].boxes.id is not None:
        current_track_ids = update_object_tracking(results, trackers)
    handle_disappeared_objects(current_track_ids, trackers)

    update_database(trackers, annotated_frame,frame)

    trackers.previous_detected_objects = copy.deepcopy(trackers.detected_objects)

    return annotated_frame


def update_object_tracking(results, trackers: TrackerManager):
    boxes = results[0].boxes.xywh.cpu()
    track_ids = results[0].boxes.id.int().cpu().tolist()
    cls_ids = results[0].boxes.cls.int().cpu().tolist()

    current_track_ids = set()
    for box, track_id, cls_id in zip(boxes, track_ids, cls_ids):
        x, y, w, h = map(float, box)
        current_track_ids.add(track_id)
        if any(obj.get_track_id() == track_id for obj in trackers.previous_detected_objects.values()):
            trackers.previous_detected_objects[track_id].position = (x, y, w, h)
            trackers.detected_objects[track_id] = trackers.previous_detected_objects[track_id]
        else :
            # Aktualisiere Klassenhistorie
            trackers.cls_id_history[track_id][cls_id] += 1

            # Berechne Entfernung und aktualisiere Verweilzeit
            if trackers.track_history[track_id]:
                lastX, lastY = trackers.track_history[track_id][-1]
                distance = ((x - lastX) ** 2 + (y - lastY) ** 2) ** 0.5
            else:
                distance = float('inf')

            if distance <= TOLERANCE:
                trackers.stay_time[track_id] += 1
            else:
                trackers.stay_time[track_id] = 0

            # Objekt hinzufügen, wenn es stabil bleibt
            if trackers.stay_time[track_id] >= ADD_REMOVE_THRESHOLD:
                position = (x, y, w, h)
                trackers.detected_objects[track_id] = DetectedObject(track_id, cls_id, position)
                trackers.disappearance_time[track_id] = 0

            # Speichere Positionshistorie
            trackers.track_history[track_id].append((x, y))
            if len(trackers.track_history[track_id]) > 30:
                trackers.track_history[track_id].pop(0)
    return current_track_ids


def handle_disappeared_objects(current_track_ids, trackers: TrackerManager):
    to_remove = []

    for _, detectOb in trackers.detected_objects.items():
        track_id = detectOb.get_track_id()
        if track_id not in current_track_ids:
            trackers.disappearance_time[track_id] += 1
            if trackers.disappearance_time[track_id] >= ADD_REMOVE_THRESHOLD:
                to_remove.append(track_id)
        else:
            trackers.disappearance_time[track_id] = 0

    for track_id in to_remove:
        del trackers.detected_objects[track_id]


def update_database(trackers: TrackerManager, annotated_frame,frame):

    if len(trackers.detected_objects.items())!=len(trackers.previous_detected_objects.items()):
        http_database_request = http_database_models.DatabaseUpdateRequest(overall_picture=encode_frame(annotated_frame),products={})
        if len(trackers.detected_objects.items())==0 and len(trackers.previous_detected_objects.items())>1:
            api_rest_client_database.delete_item_to_database(http_database_request)
        elif len(trackers.detected_objects.items())>len(trackers.previous_detected_objects.items()):
            http_database_request.products = generate_products(trackers,frame)
            api_rest_client_database.add_item_to_database(http_database_request)
        elif len(trackers.detected_objects.items())<len(trackers.previous_detected_objects.items()):
            http_database_request.products = generate_products(trackers, frame)
            api_rest_client_database.delete_item_to_database(http_database_request)


def get_necessary_class_ids(trackers: TrackerManager):
    detected_objects = trackers.detected_objects.copy()
    necessary_class_ids = []
    for _, nowDetectedOb in detected_objects.items():
        if nowDetectedOb.get_cls_id() is not None and nowDetectedOb.get_cls_id() not in necessary_class_ids:
            necessary_class_ids += [nowDetectedOb.get_cls_id()]
    return necessary_class_ids


def select_class_frames(class_id, results: []):
    filtered_boxes = results[0].boxes[results[0].boxes.cls == class_id]
    results[0].boxes = filtered_boxes
    annotated_frame = results[0].plot()
    success, buffer = cv2.imencode('.webp', annotated_frame, [cv2.IMWRITE_WEBP_QUALITY, 90])

    if success:
        base64_encoded_image = base64.b64encode(buffer).decode('utf-8')
        return base64_encoded_image
    else:
        return None

def encode_frame(frame ):
    success, buffer = cv2.imencode('.webp', frame, [cv2.IMWRITE_WEBP_QUALITY, 90])

    if success:
        base64_encoded_image = base64.b64encode(buffer).decode('utf-8')
        return base64_encoded_image
    else:
        return None

def generate_products(trackers: TrackerManager,frame):
    tmp_detected_objects = copy.deepcopy(trackers.detected_objects)
    all_products: Dict[int, Product] = {}
    detected_objects_list = list(tmp_detected_objects.values())
    while len(detected_objects_list)>0:
        item = copy.deepcopy(detected_objects_list[0])
        product_frame = copy.deepcopy(frame)
        cls_list = [cls_item for cls_item in detected_objects_list if item.get_cls_id() == cls_item.get_cls_id()]
        product_name = model.names[item.get_cls_id()]
        product_amount = len(cls_list)
        for pic_item in cls_list:
            product_frame = draw_bounding_box(product_frame,pic_item)
            detected_objects_list.remove(pic_item)

        product_picture = encode_frame(product_frame)
        all_products[item.get_cls_id()] = Product(name=product_name,amount=product_amount,picture=product_picture)
    return  all_products

def draw_bounding_box(frame, detected_object):
    x_min, y_min, x_max, y_max = detected_object.get_bounding_box()
    cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (255, 0, 0), 2)

    return frame