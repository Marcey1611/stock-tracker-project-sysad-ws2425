import logging
import os

from ultralytics import YOLO

logger = logging.getLogger(__name__)

file_location = "../../."+os.getenv('HUMAN_CHECK_MODEL')
device = os.getenv('DEVICE_TO_RUN_MODELDEVICE_TO_RUN_MODEL')
model = YOLO(file_location).to(device)


def is_human_in_frame(frame):
    results = model.predict(frame, conf=0.55, imgsz=640, verbose=False)
    filteredBoxes = results[0].boxes[results[0].boxes.cls == 0]
    results[0].boxes = filteredBoxes
    annotated_frame = results[0].plot()
    classes = results[0].boxes.cls.cpu().numpy()
    if 0 in classes:
        return True, annotated_frame
    return False, None