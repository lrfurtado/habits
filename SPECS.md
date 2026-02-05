# SPECS: Pomodoro-Style TUI Scheduler (Brainstorm)

## Purpose
Build a **terminal-first daily planner** that combines:
- Time-blocked activity scheduling
- Pomodoro-style focus/rest cycles
- Active reminders (voice + desktop notifications)
- Lightweight acknowledgements for start/end of each activity

> Note: This document is brainstorming-only and intentionally avoids implementation details.

---

## Core User Goals
1. Plan a realistic day in short, focused blocks.
2. Get reminded at configurable intervals before and during activities.
3. Never miss activity boundaries (start/end) even while multitasking.
4. Confirm awareness with quick acknowledgement actions.
5. Keep the workflow entirely usable from a TUI, with optional macOS notification support.

---

## High-Value Features

### 1) Daily Schedule Management
- Create a day plan with named activities.
- Assign each activity:
  - start time
  - expected duration
  - category/tag (work, study, admin, health, etc.)
  - optional notes and priority
- Reorder and edit activities quickly.
- Show timeline and current/next activity at a glance.

### 2) Pomodoro Mode (Per Activity)
- Attach a Pomodoro pattern to each activity (e.g., 25/5, 50/10, custom).
- Allow continuous mode (no breaks) for certain tasks.
- Track completed pomodoros per activity.
- Pause/resume cycle without losing context.

### 3) Configurable Reminder Intervals
- Pre-start reminder(s): e.g., 10 min before, 5 min before, 1 min before.
- In-progress interval nudges: e.g., every N minutes until acknowledged.
- End-of-activity reminder at scheduled end.
- Escalation path when reminders are ignored:
  - repeat cadence increases
  - voice message becomes more explicit
  - desktop notification persists/renotifies

### 4) Voice-Synthesized Alerts
- Text-to-speech reminders announcing:
  - activity name
  - current phase (start, focus block, break, end)
  - optional next action ("stand up", "switch task", etc.)
- Selectable voice profile, speech rate, and volume.
- Different alert tones/phrases by reminder type.
- Quiet-hours behavior for late-night schedules.

### 5) Start/End Acknowledgement Flow
- Require user acknowledgement for:
  - activity start
  - activity end
- Fast ack options in TUI:
  - single-key confirm
  - snooze for X minutes
  - skip/mark incomplete
  - defer to next slot
- Track late acknowledgements and missed acknowledgements.

### 6) macOS Notification Support (If Available)
- Push macOS notifications for all key events:
  - upcoming start
  - start now
  - break now
  - ending soon
  - ended
- Include contextual action hints in notification text.
- Optional repeated notifications until acknowledged in TUI.
- Graceful fallback when macOS notifications are unavailable.

### 7) TUI UX Essentials
- Main dashboard with:
  - current time
  - current activity + timer
  - next activity
  - day completion progress
- Keyboard-first controls and minimal friction navigation.
- Focus mode screen for current pomodoro only.
- Compact mode for small terminal windows.
- Clear color/status indicators (upcoming, active, overdue, completed).

### 8) Resilience and Recovery
- Recover schedule state after app restart.
- Preserve acknowledgement history and timer state.
- Handle missed time windows intelligently (catch-up suggestions).
- Offer automatic schedule reflow for delays.

### 9) Insight and Reflection
- Daily summary:
  - planned vs completed activities
  - pomodoros completed
  - total focus time
  - interruptions / snoozes
- Weekly trends to improve planning accuracy.
- Exportable logs for personal review.

### 10) Personalization and Accessibility
- Configurable sounds/phrases per event type.
- High-contrast and low-distraction display themes.
- Adjustable notification verbosity.
- Ability to disable voice while keeping desktop reminders (or vice versa).

---

## Suggested Functional Modules (Conceptual)
- Schedule Planner
- Pomodoro Engine
- Reminder Orchestrator
- Voice Alert Manager
- Notification Adapter (macOS + fallback)
- Acknowledgement Tracker
- Persistence/Session Recovery
- Daily Analytics and Reports

---

## Potential Event Types
- `activity_upcoming`
- `activity_start_due`
- `activity_started_acknowledged`
- `focus_block_end`
- `break_start`
- `break_end`
- `activity_end_due`
- `activity_ended_acknowledged`
- `activity_overdue`
- `day_summary_ready`

---

## Prioritized Brainstorm Backlog

### Must Have (MVP Brainstorm)
1. Daily schedule CRUD in TUI.
2. Activity timers + pomodoro cycles.
3. Configurable reminder intervals.
4. Voice alerts for start/end and important transitions.
5. Start/end acknowledgement with snooze.
6. macOS notifications (best effort) + fallback behavior.

### Should Have
1. Delay handling and schedule reflow suggestions.
2. Persistence and restart recovery.
3. End-of-day summary.

### Nice to Have
1. Weekly productivity trends.
2. Multiple schedule templates (weekday/weekend).
3. Context-aware reminder phrasing.

---

## Non-Goals (for now)
- Team collaboration features.
- Cloud sync across devices.
- Mobile app parity.
- Heavy project/task management complexity.

---

## Success Criteria (Product-Level)
- User can run entire day from terminal with minimal friction.
- Reminder + ack loop significantly reduces missed starts/ends.
- Voice and notification system is noticeable but not overwhelming.
- User reports improved adherence to planned daily schedule within 1–2 weeks.
