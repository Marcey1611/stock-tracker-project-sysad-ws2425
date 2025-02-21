# Detection_service

This Detection_Service gets Images over the [MQTT-Broker](../mqttBroker/Readme.md) from the [Cam Service](../cam_service/Readme.md).
From there, it tries to detect some Object.
Afterward, it provides a Livestream feed of the incoming images and also a tracked version
where the detected Objects are marked.
The Stream with bounding boxes can be reached over `http://detection-service:800/video/track` and the one without under `http://detection-service:800/video/feed`.
Additionally, it sends the detected Objects to the [Database Service](../database_service/Readme.md) to store them.

## [Docker Compose](../../../../source/detectionService/docker-compose.yml)
```yaml
services:
  detection-service:
    extends: .common

  .common:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_SERVICE_URL= http://dataBaseServiceContainer:8000
      - MQTT_BROKER_URL=stock-tracker-mosquitto
      - MQTT_BROKER_PORT=1883
      - MQTT_USERNAME=sysAdmin
      - MQTT_PASSWORD=sysAd2024
      - HUMAN_CHECK_MODEL=./app/models/humancheck/yolo11n.pt
      - DETECTION_MODEL=./app/models/detection/yolo11n.pt
      - DEVICE_TO_RUN_MODEL=cpu
      - SERVER_IP=192.168.1.192


  .common_nvidia:
    extends: .common
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [ gpu ]
    environment:
      - NVIDIA_VISIBLE_DEVICES= all
      - NVIDIA_DRIVER_CAPABILITIES= compute,video,utility,graphics
```

### Recommended Environment Variables:

If your system has the **NVIDIA Container Toolkit** you could try to replace `extends: .common`
with the `extends: .common_nvidia`.
If you're using your CPU for the YOLO Models, you should keep the models Small.
Recommended is the Nano Version of YOLO.
Else you could use what you want.

- **.common**:
  - `DATABASE_SERVICE_URL` the url where you the service could reach the [Database Service](../database_service/Readme).
  - `MQTT_BROKER_URL` the ip of the server where the [MQTT Broker](../mqttBroker/Readme.md) is running.
  - `MQTT_BROKER_PORT` the port at the server where die [MQTT Broker](../mqttBroker/Readme.md) is reachable.
  - `MQTT_USERNAME` if you're using a MQTT Broker with authentication here is the place for your username. If not, remove this environment.
  - `MQTT_PASSWORD` if you're using a MQTT Broker with authentication here is the place for your password. If not, remove this environment.
  - `HUMAN_CHECK_MODEL` the location of the YOLO Model which should detect if a person is in the Picture.
  - `DETECTION_MODEL` the location of the YOLO Model which should detect the Objects.
  - `DEVICE_TO_RUN_MODEL` if you have an NVIDIA GPU and did the NVIDIA Container Toolkit setup you could try to run the YOLO Models on the GPU by setting it to `cuda`. **IF NOT** you should keep this at `cpu`.
  - `SERVER_IP` to use the Livestream you need to set this ip to the server one where this container is running.

- **.common_nvidia**
  - `NVIDIA_VISIBLE_DEVICES` declare which gpu you want to pass through. Incase you want to pass through all your GPUs try `all`.
  - `NVIDIA_DRIVER_CAPABILITIES` declare which part of the GPU should be passed through. In case of all try `all`.

## Docker File

The Dockercontainer is based on the `python3.12-slim` image.
<br>

### Python Libraries 
The Python Libraries
that needed to bee installed afterward
where installed using the [requirements.txt](../../../../source/detectionService/requirements.txt):
 - `fastapi` used for the REST communication. [link](https://github.com/fastapi/fastapi)
 - `uvicorn[standard]` also used for the REST communication. [link](https://github.com/encode/uvicorn)
 - `ultralytics` used for the Detection(YOLO). [link](https://github.com/ultralytics)
 - `lap` used for tracking. [link](https://github.com/gatagat/lap)
 - `paho-mqtt` is used for the MQTT communication. [link](https://github.com/eclipse-paho/paho.mqtt.python)

## Code
The Code is written in Python. More information can be found [here](app/Readme.md).
