import cv2

def draw_bounding_box(frame, detected_object):
    x_min, y_min, x_max, y_max = detected_object.get_bounding_box()
    cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (216,235,49), 4)

    return frame