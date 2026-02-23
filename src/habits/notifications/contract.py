from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification_payload: dict[str, Any]) -> str:
        raise NotImplementedError

    @abstractmethod
    def cancel(self, delivery_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def capabilities(self) -> dict[str, bool]:
        raise NotImplementedError

    @abstractmethod
    def handle_callback(self, raw_event: dict[str, Any]) -> dict[str, str]:
        raise NotImplementedError
