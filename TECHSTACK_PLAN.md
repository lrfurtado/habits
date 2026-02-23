# Tech Stack Plan

## TUI Core
- **Language:** Python 3.12+
- **CLI Framework:** `typer`
- **TUI Framework:** `textual`
- **TUI Components:** `textual` built-in widgets + `textual-dev` tooling
- **Styling:** `textual` CSS + `rich`
- **Logging:** `loguru`
- **Storage:** SQLite via standard-library `sqlite3` (or `sqlmodel` if ORM ergonomics are needed)

## Notification Module (from current spec)

### Runtime and Packaging
- **Language:** Python 3.12+
- **Dependency manager:** `uv` (or `pip` + `venv` fallback)
- **Reasoning:** spec requires an external Python script and possible YouTube integration.

### Process Boundary and IPC
- **Interface:** JSON-RPC 2.0 over stdio
- **Python JSON-RPC libs:**
  - `jsonrpcserver` (server-side routing)
  - `jsonrpcclient` (if client calls are needed)
- **Reasoning:** aligns with the spec requirement to communicate over JSON-RPC on stdio between the Python TUI runtime and notification process.

### MCP Server Capability
- **Protocol:** Model Context Protocol server implemented in the same Python process
- **Library choice:** `mcp` Python SDK
- **Design:** expose MCP tools/resources for notification preview/testing and message generation while reusing the same internal notification engine.

### Notifications and Actions
- **Architecture:** channel adapter pattern
  - Keep scheduling/escalation/ack logic in a channel-agnostic orchestration layer.
  - Implement delivery platforms as pluggable adapters behind a shared interface (`send`, `cancel`, `capabilities`, callback normalization).
  - Configure channel routing per user and optionally per notification type.
- **MVP channel:** Desktop notifications via `desktop-notifier`
  - Cross-platform support and actionable buttons (`Ack`, `Snooze`, `Skip`) with callback handlers.
- **Future channels:** WhatsApp and Telegram adapters
  - Add adapters later without changing orchestration or JSON-RPC surface.
- **Audio playback:** `python-vlc`
  - Plays short alert sounds and recorded clips (including local media or stream URLs).
- **Speech synthesis (same voice, varied phrasing):** `edge-tts`
  - Stable single voice selection with dynamic templated utterances.

### YouTube Clip Support
- **Source resolution/downloading:** `yt-dlp`
- **Execution model:** fetch clip URL/stream metadata with `yt-dlp`, then play through `python-vlc`.
- **Reasoning:** robust handling of YouTube short clips required by spec.


### Long-Break Self-Care Message Selection
- **Config source:** `long_break_self_care.activities` from `ui-config.yaml`.
- **Selection strategy:** `random` (default) or `cycle` from config to choose the activity at each long break boundary.
- **Validation contract:** each `activities[*].duration_minutes` must be `<= pomodoro.long_break_minutes` during config load/validation.
- **Message rendering:** notification generator appends an optional encouragement suffix when `long_break_self_care.encouragement.enabled=true` and phrases are available.

### Scheduling, Repeats, and Escalation
- **Scheduler:** `APScheduler`
- **Usage:**
  - pre-start reminder at T-5m
  - repeated reminder jobs until acknowledgement
  - escalation cadence changes over time
  - suppression when next activity starts

### Suggested Python Dependency Set
```txt
typer
textual
rich
loguru
sqlmodel
mcp
jsonrpcserver
desktop-notifier
apscheduler
python-vlc
edge-tts
yt-dlp
pydantic
```

### Integration Contract with Python TUI
- Python TUI process is the source of truth for schedule/timer state.
- Python notification process receives events/commands over JSON-RPC stdio, for example:
  - `schedule_reminder(activity_id, starts_at, policy)`
  - `cancel_activity(activity_id)`
  - `ack(activity_id)`
  - `snooze(activity_id, duration_minutes)`
  - `skip(activity_id)`
- Python process emits JSON-RPC notifications/events back:
  - `reminder_fired`
  - `ack_timeout`
  - `action_selected`
  - `notification_error`
