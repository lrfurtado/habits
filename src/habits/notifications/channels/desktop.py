from __future__ import annotations

import uuid
from typing import Any

from habits.notifications.contract import NotificationChannel


class DesktopNotificationChannel(NotificationChannel):
    def __init__(self) -> None:
        self._active: dict[str, dict[str, Any]] = {}

    def send(self, notification_payload: dict[str, Any]) -> str:
        delivery_id = str(uuid.uuid4())
        self._active[delivery_id] = notification_payload
        print(f"[desktop] {notification_payload.get('title', 'Reminder')}: {notification_payload.get('message', '')}")
        return delivery_id

    def cancel(self, delivery_id: str) -> None:
        self._active.pop(delivery_id, None)

    def capabilities(self) -> dict[str, bool]:
        return {
            "supports_actions": True,
            "supports_audio": True,
            "supports_tts": True,
        }

    def handle_callback(self, raw_event: dict[str, Any]) -> dict[str, str]:
        action = raw_event.get("action", "ack")
        if action not in {"ack", "snooze", "skip"}:
            action = "ack"
        return {"action": action, "item_id": raw_event.get("item_id", "")}
