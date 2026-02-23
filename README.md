# Habits — Fixed-Schedule Focus & Reminder System

This repository now contains an implementation scaffold for the specifications in `Specs.md`, with configuration validated against `ui-config.schema.yaml`.

## Project layout

- `src/habits/` — application source code, intentionally split into modules for parallel agent work.
  - `config.py` — schema + business-rule validation.
  - `scheduler.py` — fixed-schedule generation and overlap enforcement.
  - `pomodoro.py` — long-break self-care selection.
  - `reminders.py` — reminder generation with escalation levels.
  - `notifications/` — channel contract, desktop adapter, orchestration.
  - `rpc/notification_server.py` — JSON-RPC over stdio notification service.
  - `tui.py` — terminal dashboard rendering.
  - `history.py` / `reporting.py` — persistent history and JSON summary export.
- `tests/` — baseline tests for schema validation + scheduling behavior.
- `requirements.txt` / `requirements-dev.txt` — runtime and development dependencies.
- `justfile` — common development, run, test, and export tasks.

## Quick start

```bash
python -m pip install -r requirements-dev.txt
just test
just run
```

## Useful commands (via `just`)

- `just install` — install runtime dependencies.
- `just dev-install` — install runtime + dev dependencies.
- `just validate-config` — run app startup path with config/schema validation.
- `just test` — execute test suite.
- `just run` — start the TUI flow.
- `just notification-server` — run JSON-RPC notification server over stdio.
- `just export-daily` / `just export-weekly` — write JSON summary outputs.

## Notes

- The scheduler enforces fixed windows and rejects overlaps.
- Appointments (recurring + one-off) are treated with precedence over template activities.
- History is append-only JSONL and summaries are exported as JSON.
- Notification routing is channel-based and currently ships with a desktop channel for MVP.
