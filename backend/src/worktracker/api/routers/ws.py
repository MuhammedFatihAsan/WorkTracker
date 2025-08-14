from __future__ import annotations

from typing import Annotated
from fastapi import APIRouter, Depends, WebSocket

from ..deps import get_ws_hub
from ...realtime.hub import WebSocketHub, hold_connection

router = APIRouter(tags=["ws"])

@router.websocket("/ws")
async def ws_public(
    ws: WebSocket,
    hub: Annotated[WebSocketHub, Depends(get_ws_hub)],
):
    await hub.connect_public(ws)
    try:
        await hold_connection(ws)
    finally:
        await hub.disconnect_public(ws)

@router.websocket("/ws/users/{user_id}")
async def ws_user_room(
    user_id: int,
    ws: WebSocket,
    hub: Annotated[WebSocketHub, Depends(get_ws_hub)],
):
    await hub.connect_user(user_id, ws)
    try:
        await hold_connection(ws)
    finally:
        await hub.disconnect_user(user_id, ws)
