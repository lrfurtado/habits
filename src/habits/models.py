from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Literal

DayName = Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
ActivityStatus = Literal["pending", "done", "not_done", "skipped"]


@dataclass(frozen=True)
class TimeBlock:
    id: str
    title: str
    start: time
    end: time
    requires_ack: bool = True


@dataclass(frozen=True)
class RecurringAppointment(TimeBlock):
    days_of_week: tuple[DayName, ...] = ()


@dataclass(frozen=True)
class OneOffAppointment(TimeBlock):
    day: date = field(default_factory=date.today)


@dataclass
class ScheduledItem:
    block: TimeBlock
    source: Literal["template", "recurring_appointment", "one_off_appointment", "break", "self_care"]
    status: ActivityStatus = "pending"
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class DayPlan:
    day: date
    items: list[ScheduledItem]
    missed_count: int = 0


@dataclass
class ReminderEvent:
    item_id: str
    when: datetime
    level: int
    message: str


@dataclass
class ActionEvent:
    action: Literal["ack", "snooze", "skip"]
    item_id: str
    at: datetime
