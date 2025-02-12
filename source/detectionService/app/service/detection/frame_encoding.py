import base64
import cv2


def encode_frame(frame ):
    success, buffer = cv2.imencode('.webp', frame, [cv2.IMWRITE_WEBP_QUALITY, 90])

    if success:
        base64_encoded_image = base64.b64encode(buffer).decode('utf-8')
        return base64_encoded_image
    else:
        return None