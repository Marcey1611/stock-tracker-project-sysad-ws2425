import cv2

camera = cv2.VideoCapture(0)

desiredWidth = 1280
desiredHeight = 720

camera.set(cv2.CAP_PROP_FRAME_WIDTH, desiredWidth)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, desiredHeight)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

frameWidth = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(f"Auflösung der Kamera: {int(frameWidth)}x{int(frameHeight)}")

def streamFrames():
    while True:
        success, frame = camera.read()  # Frame von der Kamera lesen
        if not success:
            break
        else:
            # Frame in JPEG umwandeln
            _, buffer = cv2.imencode('.jpg', frame)
            frameBytes = buffer.tobytes()
            # MJPEG-Frame erzeugen
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frameBytes + b'\r\n')