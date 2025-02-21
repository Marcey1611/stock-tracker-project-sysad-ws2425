# cam_service

The cam_service is designed to capture images using a camera and seamlessly transmit them via the [MQTT-Broker](../mqtt_broker/Readme.md) to the 
[detction_service](../detection_service/Readme.md). for further processing.


## [Docker Compose File](../../../../source/cam_service/docker-compose.yml)
```yaml
version: "3.9"
services:
  cam-service:
    build: .
    devices:
      - "/dev/video2:/dev/video0"
    environment:
      - MQTT_BROKER_URL=192.168.1.191
      - MQTT_BROKER_PORT=1883
      - MQTT_USERNAME=sysAdmin
      - MQTT_PASSWORD=sysAd2024
```

### Recommended Environment Variables:

 - **devices**:
   - `/dev/video2:/dev/video0` => Should be the camera with which you want to capture images.

 - **environment**:
   - `MQTT_BROKER_URL` => The IP of the Server where [MQTT-Broker](../mqtt_broker/Readme.md) is running.
   - `MQTT_BROKER_PORT` => The PORT of the Server where the [MQTT-Broker](../mqtt_broker/Readme.md) can be reached.
   - `MQTT_USERNAME` => The username for the MQTT-Broker. If not needed remove it.
   - `MQTT_PASSWORD` => The password for the MQTT-Broker. If not needed remove it.


## Docker File

The Dockercontainer is based on the `python3.12-slim` image.
<br>

### Python Libraries 
The Python Libraries are installed using the [requirements.txt](../../../../source/cam_service/requirements.txt):
 - `paho-mqtt` is used for the MQTT communication. [link](https://github.com/eclipse-paho/paho.mqtt.python)
 - `opencv-python-headless` is used to capture images.[link](https://github.com/opencv/opencv-python)
