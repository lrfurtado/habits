from __future__ import annotations

from datetime import date, datetime, time

from habits.models import DayPlan, OneOffAppointment, RecurringAppointment, ScheduledItem, TimeBlock
from habits.utils import overlaps, parse_hhmm

_DAY_TO_NAME = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


class SchedulingError(ValueError):
    """Raised when a schedule cannot be produced."""


def _inside_day_window(block: TimeBlock, start: time, end: time) -> bool:
    return start <= block.start < block.end <= end


def _to_time_block(raw: dict, default_requires_ack: bool = True) -> TimeBlock:
    return TimeBlock(
        id=raw["id"],
        title=raw["title"],
        start=parse_hhmm(raw["start"]),
        end=parse_hhmm(raw["end"]),
        requires_ack=raw.get("requires_ack", default_requires_ack),
    )


def _to_recurring(raw: dict) -> RecurringAppointment:
    return RecurringAppointment(
        id=raw["id"],
        title=raw["title"],
        start=parse_hhmm(raw["start"]),
        end=parse_hhmm(raw["end"]),
        requires_ack=raw.get("requires_ack", True),
        days_of_week=tuple(raw["days_of_week"]),
    )


def collect_one_off_appointments(today: date, max_entries: int) -> list[OneOffAppointment]:
    print("Add one-off appointments for today as CSV 'id,title,start,end' (empty to finish)")
    items: list[OneOffAppointment] = []
    for idx in range(max_entries):
        entry = input(f"appointment {idx + 1}> ").strip()
        if not entry:
            break
        parts = [p.strip() for p in entry.split(",")]
        if len(parts) != 4:
            print("Invalid input. Expected 4 comma-separated values.")
            continue
        block = OneOffAppointment(
            id=parts[0],
            title=parts[1],
            start=parse_hhmm(parts[2]),
            end=parse_hhmm(parts[3]),
            requires_ack=True,
            day=today,
        )
        items.append(block)
    return items


def build_day_plan(config: dict, today: date, one_offs: list[OneOffAppointment] | None = None) -> DayPlan:
    one_offs = one_offs or []
    day_name = _DAY_TO_NAME[today.weekday()]
    template = "weekday" if day_name in {"mon", "tue", "wed", "thu", "fri"} else "weekend"

    day_start = parse_hhmm(config["day_window"]["start"])
    day_end = parse_hhmm(config["day_window"]["end"])

    template_items = [ScheduledItem(block=_to_time_block(raw), source="template") for raw in config["schedule_templates"][template]]

    recurring = [
        ScheduledItem(block=_to_recurring(raw), source="recurring_appointment")
        for raw in config["appointments"]["recurring"]
        if day_name in raw["days_of_week"]
    ]
    one_off_items = [ScheduledItem(block=b, source="one_off_appointment") for b in one_offs]

    for item in template_items + recurring + one_off_items:
        if not _inside_day_window(item.block, day_start, day_end):
            raise SchedulingError(
                f"{item.block.id} violates day window {day_start.strftime('%H:%M')} - {day_end.strftime('%H:%M')}"
            )

    accepted: list[ScheduledItem] = []
    template_not_done: list[ScheduledItem] = []

    for candidate in sorted(recurring + one_off_items, key=lambda i: i.block.start):
        if any(overlaps(candidate.block.start, candidate.block.end, existing.block.start, existing.block.end) for existing in accepted):
            raise SchedulingError(f"Appointment {candidate.block.id} overlaps another appointment")
        accepted.append(candidate)

    for activity in sorted(template_items, key=lambda i: i.block.start):
        collides = [
            appt
            for appt in accepted
            if overlaps(activity.block.start, activity.block.end, appt.block.start, appt.block.end)
        ]
        if collides:
            activity.status = "not_done"
            activity.metadata["suppressed_by"] = ",".join(c.block.id for c in collides)
            template_not_done.append(activity)
            continue
        if any(overlaps(activity.block.start, activity.block.end, existing.block.start, existing.block.end) for existing in accepted):
            raise SchedulingError(f"Template activity {activity.block.id} overlaps another scheduled item")
        accepted.append(activity)

    items = sorted(accepted + template_not_done, key=lambda i: (i.block.start, i.source != "template"))
    return DayPlan(day=today, items=items, missed_count=sum(1 for item in items if item.status == "not_done"))


def current_item(plan: DayPlan, now: datetime) -> ScheduledItem | None:
    current_time = now.time()
    for item in plan.items:
        if item.block.start <= current_time < item.block.end and item.status == "pending":
            return item
    return None
