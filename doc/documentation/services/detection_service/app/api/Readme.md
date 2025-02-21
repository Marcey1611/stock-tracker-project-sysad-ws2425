# api
## api_rest_client_database.py
This file contains only one method.
### update_database_products
```python
def update_database_products(data:DatabaseUpdateRequest):
    try:
        response = requests.post(f"{url}/update_products", json=data.model_dump(), headers=headers)
        if response.status_code != 200:
            logger.error(f"Database could not process correctly:{str(data.model_dump())}")
        return True
    except Exception as e:
        logger.error(f"Error while trying to send a Request: {str(e)}")
        return False
```
This Method sends the request to the [Database Service](../../../database_service/Readme.md)

## index-feed.html and index-track.html
These files are generated with ChatGPT, and the job is to display die images which are sent with the websockets.

## video_feed_endpoints.py
ChatGPT highly influences this file.
### get(/track) or get(/feed)
```python
@router.get("/track")
async def get():
    with open("./api/index-track.html", "r") as f:
        html_content = f.read()
        html_content = html_content.replace("localhost", ip_address)
    return HTMLResponse(content=html_content)
```
This methode is doubled for the feed and for the track.
It replaces the local host in the index.hml to point to the server.

### websocket_endpoint(/track) or websocket_endpoint(/track)
```python
@router.websocket("/ws-track")
async def websocket_endpoint(websocket: WebSocket):
    from main import track_q
    await websocket.accept()
    clients.add(websocket)
    logger.info("New client connected")

    try:
        while True:
            frame = track_q.get()
            if frame:
                await websocket.send_bytes(frame)
            await asyncio.sleep(0.03)

    except WebSocketDisconnect:
        logger.info("Client disconnected")
        clients.remove(websocket)
        await websocket.close()

    except Exception as e:
        logger.error(f"Error: {e}")
        clients.remove(websocket)
        await websocket.close()
```
This methode is doubled for the feed and for the track.
Its purpose is to send Images to the Client.

