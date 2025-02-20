# NOTICE
This repository should not contain more than 100MB.

# Stock Tracker
This repository contains the Stock-Tracker application, which monitors objects on a shelf, in a fridge, or any other location within a camera’s view under sufficient lighting. The application includes a Flutter-based GUI that displays the current stock. Additionally, users receive email notifications about any changes. All data is persistently stored in a PostgreSQL database.

## Main parts

### Cam-Service
Starts the camera and connects to the MQTT-Broker (for further information check the [Readme.md](doc/documentation/services/cam_service/Readme.md) of the Cam-Services).

### MQTT-Broker
- The Cam-Service publishes on the topic **camera/uuid/image**
- The Detection-Service is subscripted to the **camera/+/image** topic

### Detection-Service
This Services is responsible for receiving the images send by the Cam-Services, the object recognision and communication with the Database-Service (for further information on the service check [Readme.md](doc/documentation/services/detection_service/Readme.md) of the Detection-Service).
The modell used for object recognision can easily be replaced (check the [docker-compose.md](source/detectionService/docker-compose.yml) of the Detection-Service for further information). 

### Database-Service
This Service manages all incoming and outgoing traffic related to the database. Additionally, it is also responsible for triggering the Mailing-Services after receiving an udpate on products from the Detection-Service (for a more detailed explanation please refer to the [Readme.md](doc/documentation/services/database_service/Readme.md) of the Database-Service). For communication, a FastAPI interface is provided (see the [api_specification.yml](/doc/documentation/services/database_service/api_specification.yml) of the Database-Service for further information on available endpoints).

### Mailing-Service
This service is responsible for preparing and sending mails to the users e-mail addres, everytime the Database-Service sends an update (for more detailed information on the Mailing-Service please refer to [Readme.md](doc/documentation/services/mailing_service/Readme.md) of the Mailing-Service). The updates are received via a FastAPI interface (for further information on the Endpoints please check the [api_specification.yml](doc/documentation/services/mailing_service/api_specification.yml) of the Mailing-Service).

### Flutter-App
As mentioned above the app provides a simple gui (website or smartphone-app), which displays all currently detected objects. The app updates itself periodically via the `/update_app` interface provided by the Database-Service (for more detailed information please referr to [Readme.md](doc/documentation/services/flutter_app/Readme.md) of the Flutter-App).

**For information on the architecture and workflow please refer to the class- and sequenz-diagramms of the respective services:**

**Cam-Service**
- [class_diagramm.puml](doc/documentation/services/cam_service/class_diagram.puml)
- [sequenz_diagramm.puml](doc/documentation/services/cam_service/sequence_diagram.puml)

**Detection-Service**
- [class_diagramm.puml](doc/documentation/services/detection_service/class_diagram.puml)

**Database-Service**
- [class_diagramm.puml](doc/documentation/services/database_service/class_diagram.puml)
- [sequenz_diagramm.puml](doc/documentation/services/database_service/sequence_diagram.puml)

**Mailing-Service**
- [class_diagramm.puml](doc/documentation/services/mailing_service/class_diagram.puml)
- [sequenz_diagramm.puml](doc/documentation/services/mailing_service/sequence_diagram.puml)

**Flutter-App**
- [class_diagramm.puml](doc/documentation/services/flutter_app/class_diagram.puml)
- [sequenz_diagramm.puml](doc/documentation/services/flutter_app/sequence_diagram.puml) 


## Getting started

### Quickstartguide Stock-Tracker app
1. Clone the gitLab repo
2. In the [docker-compose.yml](/source/cam_service/docker-compose.yml) of the Cam-Service

    - Set `MQTT_BROKER_URL` to the IP address of the device where the Detection-Service container will be run.
    - Set `/dev/video2` to the directory of your camera. 

3. In the [docker-compose.yml](/source/detectionService/docker-compose.yml) of the Detection-Service

    - Set `SERVER_IP` to the IP address of the device where the Detection-Service container will be run.

    - Set `DEVICE_TO_RUN_MODEL` if you have a NVIDIA GPU and did the NVIDIA Container Toolkit setup you could try to run the YOLO Models on the GPU by setting it to cuda. **IF NOT you should keep this at cpu.**

**If you want more information for further configutration on this step please referr to the [Readme.md](/doc/documentation/services/detection_service/Readme.md) of the Detection-Service.**

4. In the [nginx.conf](/source/stock_tracker/nginx/nginx.conf) of the Flutter-App.

    - Set the `server_name` to the IP addres of the device where the Detection-Service container will be run.

5. In the [api_config.dart](/source/stock_tracker/lib/api_config.dart) of the Flutter-App

    - Set the IP addres in `return 'http://IP:40105/api/update_app';` to the IP addres of the device where the Detection-Service container will be run. **Do this for web and emulator.**

6. In the [docker-compose.yml](/source/mailingService/docker-compose.yml) of the Mailing-Service

    - Set `RECV_MAIL` to the mail on which you would like to receive the notifications.

7. Start the [docker-compose.yml](/source/docker-compose.yml) of the project with `docker compose up` while your in the `/source` directory.
8. Start the [docker-compose.yml](/source/cam_service/docker-compose.yml) of the Cam-Service with `docker compose up` while your in the `/source/cam_service` directory.

### Stock-Tracker flutter app installation
- For a guide on how to install the app on your phone please refer to [Readme.md](/doc/documentation/services/flutter_app/Readme.md).
- The Stock-Tracker Website is available under `IP:40105`. 
- The Camerafeed can also be accessed via a Web-browser. `IP:8000/video/feed`
- Same for the Cameratrack this will show what the object recognision detects in realtime. `IP:8000/video/track` 
- Replace the IP for the for all 3 with the IP adress from step 5.


## External dependencies
- [fastapi](https://github.com/fastapi/fastapi): FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
- [uvicorn](https://github.com/encode/uvicorn): Uvicorn is an ASGI web server implementation for Python.
- [pydantic](https://github.com/pydantic/pydantic): Data validation using Python type hints.
- [requests](https://github.com/psf/requests): Requests is a simple, yet elegant, HTTP library.
- [pydantic](https://github.com/pallets/jinja): Jinja is a fast, expressive, extensible templating engine.
- [python-dotnev](https://github.com/theskumar/python-dotenv): Python-dotenv reads key-value pairs from a .env file and can set them as environment variables.
- [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy): Python SQL Toolkit and Object Relational Mapper
- [ultralytics](https://github.com/ultralytics) used for the Detection(YOLO).
- [lap](https://github.com/gatagat/lap) used for tracking.
- [paho-mqtt](https://github.com/eclipse-paho/paho.mqtt.python) is used for the MQTT communication. 
- [opencv](https://github.com/opencv/opencv-python
) Pre-built CPU-only OpenCV packages for Python. 
- [Flutter](https://github.com/flutter/flutter) Flutter is Google's SDK for crafting beautiful, fast user experiences for mobile, web, and desktop from a single codebase.
- [Riverpod](https://github.com/rrousselGit/riverpod) A reactive caching and data-binding framework.

## Build dependencies
- [Dockerfile](/source/cam_service/Dockerfile) of the Cam-Service
- [Dockerfile](/source/database/Dockerfile) of the Database
- [Dockerfile](/source/databaseService/Dockerfile) of the Database-Service
- [Dockerfile](/source/detectionService/Dockerfile) of the Detection-Service
- [Dockerfile](/source/mailingService/Dockerfile) of the Mailing-Service
- [Dockerfile](/source/stock_tracker/Dockerfile) of the Stock-Tracker app

## Authors
- Noah Preyer - 35797 - Cam-Service, Detection-Service, MQTT-Broker - @np-223996
- Mike Lachmuth - 35968 - Database-Service, Database - @ml-224300
- Marcel Eichelberger - 35768 - Initial work, Mailing-Service - @me-223965
- Manuel Walser - 35825 - Stock Tracker App - @mw-224023

## Problems and solutions
- If the Detection-Service crashes often, replace the modell with a smaler one or provide more hardware ressources 
- Changing the camera while the Detection-Services is running, will resolve in crashes. Therefore this should be avoided. Should this occure just restart the Detection-Service and then the Cam-Service.

## Systemrequirements
**Server**
- Idealy nvidia-gpu capable of running the object recognision modell
- Cpu with capable single core performance

**Cam-Service**
- Camera with computer
