import logging

from ultralytics import YOLO

model = YOLO("./service/detection/yolo11n.pt")

logger = logging.getLogger(__name__)

def isHumanInFrame(frame):
    results = model.predict(frame, conf=0.55, imgsz=640, verbose=False)
    filteredBoxes = results[0].boxes[results[0].boxes.cls == 0]
    results[0].boxes = filteredBoxes
    annotated_frame = results[0].plot()
    classes = results[0].boxes.cls.cpu().numpy()
    if 0 in classes:
        return True, annotated_frame
    return False, None