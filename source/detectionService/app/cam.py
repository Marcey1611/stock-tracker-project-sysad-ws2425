import cv2

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()  # Frame von der Kamera lesen
        if not success:
            break
        else:
            # Frame in JPEG umwandeln
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            # MJPEG-Frame erzeugen
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
