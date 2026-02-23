from pathlib import Path

from habits.config import load_and_validate


def test_example_config_validates() -> None:
    config = load_and_validate(Path("ui-config.example.yaml"), Path("ui-config.schema.yaml"))
    assert config["pomodoro"]["long_break_minutes"] == 20
