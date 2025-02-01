import base64
import logging
import cv2

logger = logging.getLogger(__name__)

def encode_frame(frame ):
    success, buffer = cv2.imencode('.webp', frame, [cv2.IMWRITE_WEBP_QUALITY, 90])

    if success:
        base64_encoded_image = base64.b64encode(buffer).decode('utf-8')
        return base64_encoded_image
    else:
        return None

def draw_bounding_box(frame, detected_object):
    x_min, y_min, x_max, y_max = detected_object.get_bounding_box()
    cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (255, 0, 0), 2)

    return frame