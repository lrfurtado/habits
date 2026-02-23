from __future__ import annotations

from datetime import time


def parse_hhmm(value: str) -> time:
    hour, minute = value.split(":", 1)
    return time(hour=int(hour), minute=int(minute))


def overlaps(start_a: time, end_a: time, start_b: time, end_b: time) -> bool:
    return max(start_a, start_b) < min(end_a, end_b)
