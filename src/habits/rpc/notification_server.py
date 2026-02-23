from __future__ import annotations

import json
import sys
from typing import Any

from habits.notifications.channels.desktop import DesktopNotificationChannel
from habits.notifications.orchestrator import NotificationOrchestrator


class JsonRpcServer:
    def __init__(self) -> None:
        self.orchestrator = NotificationOrchestrator([DesktopNotificationChannel()])

    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        method = request.get("method")
        request_id = request.get("id")
        params = request.get("params", {})

        if method == "send_notification":
            result = self.orchestrator.send_with_fallback(params)
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        if method == "cancel_notification":
            self.orchestrator.cancel(params["delivery_id"])
            return {"jsonrpc": "2.0", "id": request_id, "result": {"ok": True}}
        if method == "capabilities":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "transport": "stdio",
                    "actions": ["ack", "snooze", "skip"],
                    "channels": ["desktop"],
                    "mcp_compatible": True,
                },
            }
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }


def serve_stdio() -> None:
    server = JsonRpcServer()
    for line in sys.stdin:
        raw = line.strip()
        if not raw:
            continue
        request = json.loads(raw)
        response = server.handle(request)
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    serve_stdio()
