# Follow-up Questions (Implementation Clarifications)

## Schedule Details
1. How should activities be entered for weekday/weekend templates (manual TUI form, editable config file, or both)?
2. If an activity runs past the hard stop at 18:00, should it be force-stopped immediately at 18:00 or allowed to finish silently but marked as overrun?

## Reminder & Escalation Rules
3. What exact escalation cadence should be used after a missed acknowledgement (for example every 1 min for first 5 min, then every 30s)?
4. Should escalation affect only reminder frequency, or also sound intensity/volume?
5. For "repeat notifications with a limit," what should the numeric limit be?

## Acknowledgement Actions
6. For Snooze, what duration options are allowed (fixed values like 1/3/5 min, or customizable)?
7. When Skip is used, should the activity be marked not done immediately and all related reminders cancelled?
8. Should end-of-activity acknowledgement remain required when start acknowledgement was skipped?

## Pomodoro Execution
9. During breaks, should reminders still run for the *next scheduled activity* if it overlaps with break timing?
10. If a new scheduled activity starts mid-focus session, should the focus session be cut immediately or allowed to complete first?

## Voice & Quiet Hours
11. Should quiet hours mute both sound alerts and speech, or only speech?
12. During quiet hours, should macOS notifications still appear normally?

## TUI & Reporting
13. Do you want a dedicated "Today timeline" panel in the dashboard, or keep the dashboard compact and single-pane?
14. Should JSON exports be generated automatically at end-of-day/week, or only on manual command?
