# MQTT
## [mqtt_client.py](../../../../../../../source/detectionService/app/service/mqtt/mqtt_client.py)
The methods on_connect and on_disconnect are skipped in this doku because those are only there for logging.
<br>
The important information for the connection to the [MQTT-Broker](../../../../mqttBroker/Readme.md) is imported via the envs
```python
broker=os.getenv('MQTT_BROKER_URL')
port=int(os.getenv('MQTT_BROKER_PORT'))
username = os.getenv('MQTT_USERNAME')
password =os.getenv('MQTT_PASSWORD')
topic ="camera/+/image"
client = mqtt.Client()
```

### on_message
```python
def on_message(inner_client, userdata, msg):
    feed_q, track_q, trackers,count,model_cls_names = userdata
    camera_id = msg.topic.split('/')[1]
    frame_bytes = msg.payload
    frame = decode_frame(frame_bytes)
    if count == 0:
        init_database(frame,model_cls_names)
    frame_handling(feed_q, track_q, frame, frame_bytes, trackers)
    count = count + 1
    logger.debug(f"Nachricht von {camera_id}")
    inner_client.user_data_set((feed_q, track_q,trackers,count,model_cls_names))
```
This method takes the published message and then [decodes](../detection/Readme.md) the frame. Afterward, it is feed to the [frame handling](../detection/Readme.md).
Additionally, if the first message is published the [database init](../http_request/Readme.md) is triggert.
### mqtt_thread
```python
def mqtt_thread(feed_q,track_q):
    from service.detection.frame_detecting import model_cls_names
    init_mqtt_client()
    trackers = TrackerManager()
    count = 0
    client.user_data_set(( feed_q, track_q,trackers,count,model_cls_names))

    connected = False
    while not connected:
        connected = try_connecting()
    client.subscribe(topic)
```
The second thread which is initialized in the [main.py](../../Readme.md) calls this method.
It initializes the connection to the [MQTT Broker](../../../../mqttBroker/Readme.md) with the init_mqtt_client and
includes the queues and the [TrackManager](../../entities/detection/Readme.md) to be available in the on_message methode.
It also tries to connect to [MQTT Broker](../../../../mqttBroker/Readme.md) until it successes.
### init_mqtt_client
```python
def init_mqtt_client():
    if len(broker) == 0 or port == 0:
        logging.info("Missing values to connect to Broker")
        sys.exit()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    if username is not None and password is not None:
        client.username_pw_set(username, password)
```
This the method sets up the connection to the [MQTT Broker](../../../../mqttBroker/Readme.md).
If the port and the ip length are 0, it kills the container.
Additionally, it sets the username and password if they are set in the [docker-compose.yml](../../../Readme).
### try_connecting
```python
def try_connecting():
    try:
        logger.info("Versuche Verbindung zum Broker...")
        client.connect(broker, port, 60)
        client.loop_start()
        return True
    except Exception as e:
        logger.debug(f"Verbindungsfehler: {e}. Neuer Versuch in 10 Sekunden...")
        time.sleep(10)
        return False
```
This is one connection-try. If it fails, it waits 10 seconds.
