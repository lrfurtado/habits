from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal


def export_summary(history_file: Path, output_file: Path, period: Literal["daily", "weekly"] = "daily") -> None:
    if not history_file.exists():
        output_file.write_text(json.dumps({"period": period, "entries": 0, "metrics": {}}), encoding="utf-8")
        return

    rows = [json.loads(line) for line in history_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        output_file.write_text(json.dumps({"period": period, "entries": 0, "metrics": {}}), encoding="utf-8")
        return

    latest = datetime.fromisoformat(rows[-1]["day"])
    window_days = 1 if period == "daily" else 7
    start = latest - timedelta(days=window_days - 1)
    filtered = [r for r in rows if datetime.fromisoformat(r["day"]) >= start]

    counters = Counter()
    deep_focus_minutes = 0
    interruptions = 0
    for row in filtered:
        for item in row["items"]:
            counters[item["status"]] += 1
            if "deep" in item["id"] and item["status"] == "done":
                start_t = datetime.strptime(item["start"], "%H:%M")
                end_t = datetime.strptime(item["end"], "%H:%M")
                deep_focus_minutes += int((end_t - start_t).total_seconds() // 60)
            if item["status"] == "not_done" and item["source"] in {"recurring_appointment", "one_off_appointment"}:
                interruptions += 1

    total = sum(counters.values()) or 1
    summary = {
        "period": period,
        "entries": len(filtered),
        "metrics": {
            "completion_rate": counters["done"] / total,
            "deep_focus_minutes": deep_focus_minutes,
            "missed_acknowledgements": counters["not_done"],
            "interruptions": interruptions,
        },
    }
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
