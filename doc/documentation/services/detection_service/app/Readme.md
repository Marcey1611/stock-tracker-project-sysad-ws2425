# APP-Folder
This folder contains the whole Python code.
The Folders are:
- [api](api/Readme.md) this folder Contains everything related to the REST communication.
- [entities](entities/Readme.md) here are all the Classes stored which we convert into Objects.
- [models](models/Readme.md) this is the place where you should put your models.
- [services](services/Readme.md) the services which make this container work are stored here.


## [main.py](../../../../../source/detectionService/app/main.py)
This file is our starting point.
There the FastAPI app is initialized to allow CORS transactions
as well as making the Livestreams available by adding the router from [video_feed_endpoints](api/Readme.md). 
```python
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(videoRouter2, prefix="/video", tags=["video"])
```
It's clear that Python is singed threaded, but to achieve a partially parallelized code, a second thread is added
to take over the [MQTT communication](services/mqtt/Readme.md) and the detection.
To exchange the pictures from one thread to the other queues are added with the Queue-size 1
to only keep the most recent image.

```python
feed_q = Queue(maxsize=1)
track_q = Queue(maxsize=1)

thread_mqtt=threading.Thread(target=mqtt_thread,args=(feed_q,track_q))
thread_mqtt.daemon = True
thread_mqtt.start()
```

Debuging is done using the [logging](https://docs.python.org/3/library/logging.html) library.
This configuration allows detailed debuging up to the funktionname.
```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)
```
