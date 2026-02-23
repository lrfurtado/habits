from datetime import date
from pathlib import Path

from habits.config import load_and_validate
from habits.models import OneOffAppointment
from habits.scheduler import SchedulingError, build_day_plan
from habits.utils import parse_hhmm


def test_appointment_precedence_marks_template_not_done() -> None:
    config = load_and_validate(Path("ui-config.example.yaml"), Path("ui-config.schema.yaml"))
    plan = build_day_plan(
        config,
        today=date(2025, 1, 6),
        one_offs=[
            OneOffAppointment(
                id="doctor",
                title="Doctor",
                start=parse_hhmm("11:45"),
                end=parse_hhmm("12:15"),
            )
        ],
    )
    suppressed = [i for i in plan.items if i.block.id == "deep_work_1"][0]
    assert suppressed.status == "not_done"


def test_reject_one_off_outside_window() -> None:
    config = load_and_validate(Path("ui-config.example.yaml"), Path("ui-config.schema.yaml"))
    try:
        build_day_plan(
            config,
            today=date(2025, 1, 6),
            one_offs=[
                OneOffAppointment(
                    id="late",
                    title="Late",
                    start=parse_hhmm("18:10"),
                    end=parse_hhmm("18:30"),
                )
            ],
        )
        raise AssertionError("Expected SchedulingError")
    except SchedulingError:
        pass
