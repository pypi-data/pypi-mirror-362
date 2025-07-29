import uuid
import asyncio
from fastapi import WebSocket, WebSocketDisconnect, FastAPI
from typing import Optional, Dict, Any, Callable, Type
from .datas import (
    GetDomSnapshotResponse, GetRecentRequestResponsePairsResponse, GrabScreenshotRequest, GrabScreenshotResponse,
    GetRecentConsoleLogsRequest, GetRecentConsoleLogsResponse,
    FetchExtraInfoForContextItemRequest, FetchExtraInfoForContextItemResponse,
    WSBaseMessage
)
import json

# Global state for the Chrome extension bridge
chrome_ws: Optional[WebSocket] = None
pending_ws_requests: Dict[str, asyncio.Future] = {}

# Message type -> response model class
RESPONSE_MODELS: Dict[str, Type[WSBaseMessage]] = {
    "grab_screenshot": GrabScreenshotResponse,
    "get_recent_console_logs": GetRecentConsoleLogsResponse,
    "fetch_extra_info_for_context_item": FetchExtraInfoForContextItemResponse,
    "get_dom_snapshot":GetDomSnapshotResponse,
    "get_recent_request_response_pairs":GetRecentRequestResponsePairsResponse,
    # Add more as needed
}

def setup_chrome_ext_bridge(app: FastAPI):
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        global chrome_ws
        chrome_ws = websocket
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                print(f"[chrome_ext_bridge] Received WS message: {data}")
                try:
                    msg_dict = json.loads(data)
                    msg_type = msg_dict.get("type")
                    request_id = msg_dict.get("request_id")
                    print(f"[chrome_ext_bridge] Parsed type: {msg_type}, request_id: {request_id}")
                    model_cls = RESPONSE_MODELS.get(msg_type)
                    if model_cls and request_id in pending_ws_requests:
                        msg = model_cls.parse_obj(msg_dict)
                        pending_ws_requests[request_id].set_result(msg)
                        print(f"[chrome_ext_bridge] Matched and set result for request_id: {request_id}")
                    else:
                        print(f"[chrome_ext_bridge] No match for type: {msg_type}, request_id: {request_id}")
                except Exception as e:
                    print(f"[chrome_ext_bridge] Error parsing WS message: {e}")
                    continue
        except WebSocketDisconnect:
            chrome_ws = None

async def send_ws_request(request_model: WSBaseMessage, timeout: float = 10.0) -> WSBaseMessage:
    if chrome_ws is None:
        raise RuntimeError("Chrome extension is not connected")
    request_id = str(uuid.uuid4())
    request_model.request_id = request_id
    future = asyncio.get_event_loop().create_future()
    pending_ws_requests[request_id] = future
    await chrome_ws.send_text(request_model.json())
    try:
        response = await asyncio.wait_for(future, timeout=timeout)
        return response
    finally:
        del pending_ws_requests[request_id] 