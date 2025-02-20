import asyncio
import logging
import os

from fastapi import APIRouter
from starlette.responses import StreamingResponse, HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

router = APIRouter()
clients = set()

logger = logging.getLogger(__name__)

ip_address=os.getenv('SERVER_IP')


@router.get("/feed")
async def get():
    # Die HTML-Seite für den Client zurückgeben
    with open("./api/index-feed.html", "r") as f:
        html_content = f.read()
        html_content = html_content.replace("localhost", ip_address)
    return HTMLResponse(content=html_content)

@router.websocket("/ws-feed")
async def websocket_endpoint(websocket: WebSocket):
    from main import feed_q
    await websocket.accept()
    clients.add(websocket)
    logger.info("New client connected")

    try:
        while True:
            frame = feed_q.get()
            if frame:
                await websocket.send_bytes(frame)
            await asyncio.sleep(0.03)

    except WebSocketDisconnect:
        # Wenn der Client die Verbindung trennt
        logger.info("Client disconnected")
        clients.remove(websocket)  # Entferne den Client aus der Liste
        await websocket.close()

    except Exception as e:
        # Allgemeine Fehlerbehandlung
        logger.error(f"Error: {e}")
        clients.remove(websocket)
        await websocket.close()


@router.get("/track")
async def get():
    # Die HTML-Seite für den Client zurückgeben
    with open("./api/index-track.html", "r") as f:
        html_content = f.read()
        html_content = html_content.replace("localhost", ip_address)
    return HTMLResponse(content=html_content)

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
        # Allgemeine Fehlerbehandlung
        logger.error(f"Error: {e}")
        clients.remove(websocket)
        await websocket.close()