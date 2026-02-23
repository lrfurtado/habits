from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from habits.utils import parse_hhmm


class ConfigError(ValueError):
    """Raised when configuration fails schema or business validation."""


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_config(config: dict[str, Any], schema: dict[str, Any]) -> None:
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(config), key=lambda e: list(e.path))
    if errors:
        details = "; ".join(f"{'/'.join(str(p) for p in err.path)}: {err.message}" for err in errors)
        raise ConfigError(f"Schema validation failed: {details}")

    long_break = config["pomodoro"]["long_break_minutes"]
    for activity in config["long_break_self_care"]["activities"]:
        if activity["duration_minutes"] > long_break:
            raise ConfigError(
                f"long_break_self_care activity '{activity['id']}' duration_minutes "
                f"({activity['duration_minutes']}) exceeds pomodoro.long_break_minutes ({long_break})"
            )

    day_start = parse_hhmm(config["day_window"]["start"])
    day_end = parse_hhmm(config["day_window"]["end"])
    if day_start >= day_end:
        raise ConfigError("day_window.start must be earlier than day_window.end")


def load_and_validate(config_path: Path, schema_path: Path) -> dict[str, Any]:
    schema = load_yaml(schema_path)
    config = load_yaml(config_path)
    validate_config(config, schema)
    return config
