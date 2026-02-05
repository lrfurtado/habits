# Tech Stack Plan

## TUI Core
- **Language:** Go
- **CLI Framework:** `github.com/spf13/cobra`
- **TUI Framework:** `github.com/charmbracelet/bubbletea`
- **TUI Components:** `github.com/charmbracelet/bubbles`
- **Styling:** `github.com/charmbracelet/lipgloss`
- **Logging:** `go.uber.org/zap`
- **Storage:** SQLite via `github.com/mattn/go-sqlite3`

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
- **Reasoning:** aligns with the spec requirement to communicate over JSON-RPC on stdio between Go TUI and notification process.

### MCP Server Capability
- **Protocol:** Model Context Protocol server implemented in the same Python process
- **Library choice:** `mcp` Python SDK
- **Design:** expose MCP tools/resources for notification preview/testing and message generation while reusing the same internal notification engine.

### Notifications and Actions
- **Desktop notifications:** `desktop-notifier`
  - Cross-platform support and actionable buttons (`Ack`, `Snooze`, `Skip`) with callback handlers.
- **Audio playback:** `python-vlc`
  - Plays short alert sounds and recorded clips (including local media or stream URLs).
- **Speech synthesis (same voice, varied phrasing):** `edge-tts`
  - Stable single voice selection with dynamic templated utterances.

### YouTube Clip Support
- **Source resolution/downloading:** `yt-dlp`
- **Execution model:** fetch clip URL/stream metadata with `yt-dlp`, then play through `python-vlc`.
- **Reasoning:** robust handling of YouTube short clips required by spec.

### Notification Delivery Scope
- The Python module is a delivery engine only: render and dispatch notifications requested by the Go app.
- It does **not** own Pomodoro cadence, timer progression, schedule logic, or suppression policy decisions.
- If retries/escalation are used, they are passed in as explicit per-notification policy from the Go app.

### Suggested Python Dependency Set
```txt
mcp
jsonrpcserver
desktop-notifier
apscheduler
python-vlc
edge-tts
yt-dlp
pydantic
```

### Integration Contract with Go TUI
- Go process is the source of truth for Pomodoro, schedule, timer, and activity state.
- Python notification process receives delivery-oriented commands over JSON-RPC stdio, for example:
  - `notify(event_id, channel_payload, actions, retry_policy)`
  - `cancel_notification(event_id)`
  - `set_quiet_hours(policy)`
- Python process emits delivery/action events back:
  - `notification_sent`
  - `notification_failed`
  - `action_selected`
