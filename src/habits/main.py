from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from habits.config import load_and_validate
from habits.history import persist_day_plan
from habits.reporting import export_summary
from habits.scheduler import build_day_plan, collect_one_off_appointments
from habits.tui import render_dashboard


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fixed-schedule habits app")
    parser.add_argument("--config", default="ui-config.example.yaml")
    parser.add_argument("--schema", default="ui-config.schema.yaml")
    parser.add_argument("--history", default="data/history.jsonl")
    parser.add_argument("--export", choices=["daily", "weekly"], default="daily")
    parser.add_argument("--no-prompt", action="store_true", help="Disable one-off appointment prompt")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_and_validate(Path(args.config), Path(args.schema))

    today = date.today()
    one_offs = []
    prompt_cfg = config["appointments"]["daily_prompt"]
    if prompt_cfg["enabled"] and prompt_cfg["prompt_on_app_open"] and not args.no_prompt:
        one_offs = collect_one_off_appointments(today, prompt_cfg["max_entries"])

    plan = build_day_plan(config, today=today, one_offs=one_offs)
    render_dashboard(plan)

    history_file = Path(args.history)
    persist_day_plan(plan, history_file)
    export_summary(history_file, Path(f"data/{args.export}-summary.json"), period=args.export)


if __name__ == "__main__":
    main()
