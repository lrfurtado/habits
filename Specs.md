# ⏱️ Fixed-Schedule Focus & Reminder System — Specification

## 1. Schedule & Workflow
- Scheduling model: Fixed-time activities only (no flexible or shifting blocks).
- Overlap handling: Overlapping activities are strictly prevented.
- Templates: Two reusable schedules:
  - Weekday schedule
  - Weekend schedule
- Day window:
  - Start: `11:30`
  - End: `18:00` (hard stop)

## 2. Pomodoro System
- Default focus/break: `25` minutes focus / `5` minutes break.
- Scope: Global (same for all activities).
- Long break: `20` minutes after every `3` focus sessions.
- Long-break self-care plan:
  - The system loads a configurable **set of self-care activities** from the config file.
  - At each long break, the system selects one activity from this set.
  - Every configured self-care activity must be completable within the configured long-break duration.
  - Spoken/contextual notification text for the selected activity may append an encouragement phrase at the end.

## 3. Reminder Behavior
- Pre-start reminders: `1` reminder, `5` minutes before start.
- Unacknowledged reminders: Continue indefinitely until acknowledged.
- Escalation:
  - Increased frequency
  - Different wording over time
- Suppression rule:
  - When the next activity starts, previous reminders are suppressed.
  - Previous activity is marked **not done**.

## 4. Notification Model
- Channel architecture: Notification delivery must be channel-based, transport-agnostic, and extensible.
- Alert types:
  - Short alert sounds
  - Funny recorded youtube short clip
  - Spoken contextual messages (especially for reminders)
- Voice model: Same voice, different phrasing per event.
- Quiet hours: Configurable quiet / do-not-disturb blocks.
- Notification scope: Selective (not all alerts, not only critical).
- Actions supported: Actionable buttons (for example: Ack, Snooze, Skip).
- Repeat behavior: Repeat notifications with a limit until acknowledged.
- Initial channel: Desktop/local notifications (required for MVP).
- Future channels: WhatsApp and Telegram must be supported through the same channel contract without redesigning scheduler, escalation, or acknowledgement logic.

## 5. Notification model implementation details
- This module must be runnable as an external Python script.
- Because of possible YouTube integration, this module must be implemented in Python.
- For communicating with it, use JSON-RPC over stdio.
- This module on its own should be able to act as an MCP server.
- Internal design must separate **notification policy/orchestration** from **delivery channels**.
  - Policy/orchestration responsibilities:
    - reminder timing
    - escalation cadence and wording changes
    - acknowledgement state
    - suppression when next activity starts
  - Delivery channel responsibilities:
    - send/render the message to a specific platform
    - expose available actions (Ack, Snooze, Skip) where supported
    - map external platform callbacks/webhooks back into normalized actions
- Define a channel interface/contract so each channel is pluggable:
  - `send(notification_payload) -> delivery_id`
  - `cancel(delivery_id)`
  - `capabilities() -> {supports_actions, supports_audio, supports_tts, supports_media, ...}`
  - `handle_callback(raw_event) -> normalized_action`
- Notification payloads must be normalized before delivery and include:
  - stable `notification_id` for correlation/idempotency
  - `activity_id`, `event_type`, and escalation stage
  - message variants (`title`, `body`, optional `tts_text`)
  - optional media references (sound file, clip URL)
  - action definitions (Ack/Snooze/Skip) for channels that support buttons
- Channel selection/routing must be configuration-driven (per user and optionally per notification type).
- MVP implementation includes only Desktop channel adapter; WhatsApp and Telegram adapters are deferred but must fit the same contract.
- Channel failures must not crash orchestration; they should emit structured errors and allow fallback channels when configured.
## 6. Acknowledgement Model
- Acknowledgement requirement: Mixed / configurable per activity.
- Quick actions:
  - Snooze
  - Skip
- Snooze behavior:
  - Temporary only
  - Does not shift the schedule
- implement this model on the TUI itself

## 7. TUI (Terminal UI) Experience
- Main dashboard includes:
  - Current timer
  - Day progress
  - Next activity
  - Overdue / missed count
- Keybindings: Vim-like.
- Visual style: Color-coded, status-heavy interface.

## 8. Data, History & Reporting
- History retention: Forever.
- Metrics tracked:
  - Completion rate
  - Deep-focus minutes
  - Missed acknowledgements
  - Interruptions
- Export: JSON only (daily / weekly summaries).

## 9. Reliability & Edge Cases
- App restart behavior: Timers resume from wall-clock time.
- Missed activities: Always marked **not done** (no prompt, no reschedule).
- Timezone handling: None (schedule stays fixed to original timezone).

## 10. Future Scope (Explicitly Excluded)
- ❌ Calendar integration (Apple / Google)
- ❌ Habit streak tracking
- ❌ Ambient sounds or focus music

## 11. Long-Break Self-Care Configuration Contract
- Config must define a dedicated `long_break_self_care` block.
- The block includes:
  - `activities`: a non-empty list of candidate activities/messages to perform during long break.
  - `selection_strategy`: how to pick the next activity (`random` or deterministic cycle).
  - `encouragement` settings for optional positive suffixes.
- Validation rule:
  - Each configured self-care activity includes a `duration_minutes` value.
  - `duration_minutes` must be less than or equal to configured `pomodoro.long_break_minutes`.
