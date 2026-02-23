from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from habits.models import DayPlan


def persist_day_plan(plan: DayPlan, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "day": plan.day.isoformat(),
        "missed_count": plan.missed_count,
        "items": [
            {
                "id": item.block.id,
                "title": item.block.title,
                "start": item.block.start.strftime("%H:%M"),
                "end": item.block.end.strftime("%H:%M"),
                "source": item.source,
                "status": item.status,
                "requires_ack": item.block.requires_ack,
                "metadata": item.metadata,
            }
            for item in plan.items
        ],
    }
    with output_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")
