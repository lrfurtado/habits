from __future__ import annotations

from typing import Any

from habits.notifications.contract import NotificationChannel


class NotificationOrchestrator:
    def __init__(self, channels: list[NotificationChannel]) -> None:
        self.channels = channels

    def send_with_fallback(self, payload: dict[str, Any]) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        for channel in self.channels:
            try:
                delivery_id = channel.send(payload)
                return {"ok": True, "delivery_id": delivery_id, "channel": channel.__class__.__name__, "errors": errors}
            except Exception as exc:  # noqa: BLE001
                errors.append({"channel": channel.__class__.__name__, "error": str(exc)})
        return {"ok": False, "errors": errors}

    def cancel(self, delivery_id: str) -> None:
        for channel in self.channels:
            try:
                channel.cancel(delivery_id)
            except Exception:
                continue
