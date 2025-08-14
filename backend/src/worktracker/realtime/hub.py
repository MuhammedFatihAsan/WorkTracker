from __future__ import annotations

import asyncio
from typing import Dict, Set, Optional

import anyio
from fastapi import WebSocket, WebSocketDisconnect


class WebSocketHub:
    """
    Basit WS hub:
      - public oda: /ws
      - kullanıcı odası: /ws/users/{user_id}
    Servis içinden sync olarak çağrılan publish_* metodları,
    içeride async yayınları güvenli şekilde tetikler (anyio.from_thread.run).
    """

    def __init__(self) -> None:
        # websocket set'leri
        self._public_clients: Set[WebSocket] = set()
        self._user_rooms: Dict[int, Set[WebSocket]] = {}
        # eşzamanlı erişim için lock
        self._lock = asyncio.Lock()

    # ---------- bağlan/ayrıl ----------

    async def connect_public(self, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._public_clients.add(ws)

    async def disconnect_public(self, ws: WebSocket) -> None:
        async with self._lock:
            self._public_clients.discard(ws)

    async def connect_user(self, user_id: int, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            room = self._user_rooms.setdefault(user_id, set())
            room.add(ws)

    async def disconnect_user(self, user_id: int, ws: WebSocket) -> None:
        async with self._lock:
            room = self._user_rooms.get(user_id)
            if room:
                room.discard(ws)
                if not room:
                    self._user_rooms.pop(user_id, None)

    # ---------- publish (sync entry) ----------

    def publish_task_created(self, task_id: int, assignee_id: Optional[int]) -> None:
        """
        Servis katmanı sync çalışırken güvenle çağrılır.
        Async yayın _publish_* içinde yapılır.
        """
        anyio.from_thread.run(self._publish_task_created_async, task_id, assignee_id)

    def publish_task_updated(self, task_id: int) -> None:
        anyio.from_thread.run(self._publish_task_updated_async, task_id)

    # ---------- publish (async core) ----------

    async def _publish_task_created_async(self, task_id: int, assignee_id: Optional[int]) -> None:
        payload = {"type": "task_created", "task_id": task_id, "assignee_id": assignee_id}
        targets: Set[WebSocket] = set()
        async with self._lock:
            targets |= self._public_clients
            if assignee_id is not None and assignee_id in self._user_rooms:
                targets |= self._user_rooms[assignee_id]
        await self._broadcast_json(targets, payload)

    async def _publish_task_updated_async(self, task_id: int) -> None:
        payload = {"type": "task_updated", "task_id": task_id}
        async with self._lock:
            targets = set(self._public_clients)
        await self._broadcast_json(targets, payload)

    # ---------- yardımcı ----------

    async def _broadcast_json(self, clients: Set[WebSocket], message: dict) -> None:
        dead: Set[WebSocket] = set()
        for ws in list(clients):
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        if dead:
            async with self._lock:
                for ws in dead:
                    self._public_clients.discard(ws)
                # user odalarından da temizle
                for room in self._user_rooms.values():
                    room.discard(ws)


async def hold_connection(ws: WebSocket) -> None:
    """
    Bağlı websocket'i açık tutmak için basit loop.
    İstemci bir şey göndermezse bile ping/pong’lar bağlantıyı yaşatır.
    """
    try:
        while True:
            # istemciden mesaj bekle (gelen mesajı çöpe atıyoruz)
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    except Exception:
        # loglamak istersen burada logla
        pass
