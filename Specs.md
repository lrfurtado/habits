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
- Alert types:
  - Short alert sounds
  - Funny recorded youtube short clip
  - Spoken contextual messages (especially for reminders)
- Voice model: Same voice, different phrasing per event.
- Quiet hours: Configurable quiet / do-not-disturb blocks.
- Notification scope: Selective (not all alerts, not only critical).
- Actions supported: Actionable buttons (for example: Ack, Snooze, Skip).
- Repeat behavior: Repeat notifications with a limit until acknowledged.
## 5. Notification model implementation details
- this module should be runnable as a external python script
- because of possible youtube integration this module needs to be in python
- for communicating with it lets json rpc over strio
- this module on its own should be able to act as a mcp server
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
