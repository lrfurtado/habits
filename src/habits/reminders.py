from __future__ import annotations

from datetime import datetime, timedelta

from habits.models import ReminderEvent, ScheduledItem

_ESCALATION_STEPS = {
    "none": [10],
    "mild": [10, 7, 5],
    "moderate": [10, 7, 5, 3],
    "aggressive": [8, 5, 3, 2],
}


def reminder_plan_for_item(item: ScheduledItem, config: dict, start_at: datetime) -> list[ReminderEvent]:
    pre_start = config["reminders"]["pre_start"]
    events = [
        ReminderEvent(
            item_id=item.block.id,
            when=start_at - timedelta(minutes=pre_start["minutes_before_start"]),
            level=0,
            message=f"Upcoming: {item.block.title} starts at {item.block.start.strftime('%H:%M')}",
        )
    ]

    escalation = config["reminders"]["escalation"]["frequency_increase"]
    cadence = _ESCALATION_STEPS[escalation]
    current = start_at
    for level, minutes in enumerate(cadence, start=1):
        current += timedelta(minutes=minutes)
        events.append(
            ReminderEvent(
                item_id=item.block.id,
                when=current,
                level=level,
                message=f"Reminder level {level}: Please acknowledge '{item.block.title}'.",
            )
        )
    return events
