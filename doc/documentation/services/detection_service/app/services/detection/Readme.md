# Detection
This is the collection of files which contribute to the Objectdetection
## frame_codings
This is the summary of the en- and decodings.
### encode_frame
```python
def encode_frame(frame):
    success, buffer = cv2.imencode('.webp', frame, [cv2.IMWRITE_WEBP_QUALITY, 90])
    if success:
        base64_encoded_image = base64.b64encode(buffer)
        return base64_encoded_image
    else:
        return None
```
The pictures that are sent to the [Database Service](../../../../database_service/Readme.md) are base64 encoded.
To save space, it is also transformed into a `.webp` format. Furthermore, the quality of the image is also decreased. 
### decode_frame
```python
def decode_frame(frame_bytes):
    np_arr = np.frombuffer(frame_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
```
To send the bytes over mqtt, the [Cam Service](../../../../cam_service/Readme.md) turns the frame into bytes. This methode converts the bytes back to a frame.
## frame_detecting
```python
file_location = "../../."+os.getenv('DETECTION_MODEL')
device = os.getenv('DEVICE_TO_RUN_MODEL')

model = YOLO(file_location).to(device)
```
The location of the Model is set together from the and the device [docker-compose.yml](../../../Readme.md).
If you're using a YOLO model, it can be downloaded automatically from [ultralytics](https://github.com/ultralytics/ultralytics?tab=readme-ov-file). Only Model with the `.pt` ending is supportet.

### frame_detection
```python
def frame_detection(frame, trackers:TrackerManager):
    results = model.track(frame, conf=0.55, imgsz=640, verbose=False,persist=True)
    annotated_frame = results[0].plot()

    current_track_ids = set()
    if results[0].boxes is not None and results[0].boxes.id is not None:
        current_track_ids = update_object_tracking(results, trackers)
    handle_disappeared_objects(current_track_ids,trackers)

    update_database(trackers,annotated_frame,frame)

    trackers.previous_detected_objects = trackers.detected_objects.copy()
    return annotated_frame
```
In this method does the object detection. 
The result is fed into these methods update_object_tracking, handle_disappeared_objects and update_database which are explained [here](../tracking/Readme.md).
In the end, the previously detected objects of the [TrackingManager](../../entities/detection/Readme.md) are updated.
## frame_drawings
### draw_bounding_box
```python
def draw_bounding_box(frame, detected_object):
    x_min, y_min, x_max, y_max = detected_object.get_bounding_box()
    cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (49,235,216), 8)
    return frame
```
This methode does draw rectangles into an image. The rectangles are inserted from the generate_products out of the [http_request_service.py](../http_request/Readme.md)
## frame_handling
### frame_handling
```python
def frame_handling(feed_q:Queue, track_q:Queue, frame, frame_bytes, trackers:TrackerManager):

    human_check, annotated_frame = is_human_in_frame(frame)
    if human_check:
        put_frames_into_queue(frame, frame_bytes, feed_q)
        put_frames_into_queue(annotated_frame, None, track_q)

    else:
        annotated_frame = frame_detection(frame, trackers)

        put_frames_into_queue(frame, frame_bytes, feed_q)
        put_frames_into_queue(annotated_frame, None, track_q)
```
The on_message method forwards the frame into this funktion.
It then detects with the is_human_in_frame function if there is a person standing in the frame. 
In both cases, the images are put into the queue using the method below.
The difference is if there is no Person in the frame then enters the frame_detection.
### put_frames_into_queue
```python
def put_frames_into_queue(frame, frame_bytes, frame_queue: Queue):
    if frame_bytes is None:
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        _, buffer = cv2.imencode('.jpg', frame, encode_param)
        frame_bytes = buffer.tobytes()

    try:
        if frame_queue.full():
            frame_queue.get_nowait()
        frame_queue.put_nowait(frame_bytes)
    except Exception as e:
        print(f"Error while putting frame in queue: {e}")
```
This method puts the frames into the queue so that the livestream is able to see them.
They will be removed from the [video_feed_endpoints.py](../../api/Readme.md)
## human_checking
```python
file_location = "../../."+os.getenv('HUMAN_CHECK_MODEL')
device = os.getenv('DEVICE_TO_RUN_MODEL')
model = YOLO(file_location).to(device)
```
This is the same as in the frame_detection.py where the Model is loaded from the docker-compose.yml as well as the device.

### is_human_in_frame
```python
def is_human_in_frame(frame):
    results = model.predict(frame, conf=0.55, imgsz=640, verbose=False)
    filtered_boxes = results[0].boxes[results[0].boxes.cls == 0]
    results[0].boxes = filtered_boxes
    annotated_frame = results[0].plot()
    classes = results[0].boxes.cls.cpu().numpy()
    if 0 in classes:
        return True, annotated_frame
    return False, None
```
This method checks if a person is in the frame.
It helps to keep track of the Objects if a Person covers them by stepping into to frame.