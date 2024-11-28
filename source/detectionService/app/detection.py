import cv2
from cam import camera
from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("bestN.pt")

def object_detection():
    while camera.isOpened():
        success, frame = camera.read()
        if success:
            results = model.track(frame, persist=True,conf=0.5,iou=0.4,verbose=False,device="cpu")

            annotated_frame = results[0].plot()

            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            if not ret:
                break

            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        else:
            break

    # Release the video capture object and close the display window
    camera.release()
    cv2.destroyAllWindows()