# CamService
Der CamService hat die Aufgabe Bilder mit einer Kamera aufzunehmen und diese dann über [MQTTBrocker](https://google.com)
an den [DetctionService](https://google.com).

Der Service darf erst gestartet werden wenn der [MQTTBrocker](https://google.com) auch läuft.

## [Docker Compose File](https://google.com)
```yaml
version: "3.9"
services:
  cam-service:
    build: .
    devices:
      - "/dev/video2:/dev/video0"
    environment:
      - MQTT_BROKER_URL=192.168.2.15
      - MQTT_BROKER_PORT=1883
```

Parameter die Angepasst werden müssen:

 - **devices**:
   - `/dev/video2:/dev/video0` => Die Address der Kamera. Wird benötigt um die Bild aufzunehmen.

 - **environment**:
   - `MQTT_BROKER_URL` => Ip auf welchem der [MQTTBrocker](https://google.com) erreichbar ist.
   - `MQTT_BROKER_PORT` => Port auf welchem der [MQTTBrocker](https://google.com) erreichbar ist.

## Docker File

Der Dockercontainer basiert auf einem `python3.12-slim` Image.
<br>

### Python Bibliotheken
Die Python Bibliotheken werden über die [requiremnets.txt](./../../../source/camService/requirements.txt):
 - `paho-mqtt` für die MQTT kommunikation. 
 - `opencv-python-headless` verwendet.
