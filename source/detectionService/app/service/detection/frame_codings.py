import base64
import cv2
import numpy as np


def encode_frame(frame):
    success, buffer = cv2.imencode('.webp', frame, [cv2.IMWRITE_WEBP_QUALITY, 90])
    if success:
        base64_encoded_image = base64.b64encode(buffer)
        return base64_encoded_image
    else:
        return None

def decode_frame(frame_bytes):
    np_arr = np.frombuffer(frame_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)