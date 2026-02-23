from __future__ import annotations

import random


def pick_self_care_activity(config: dict, completed_focus_sessions: int) -> dict:
    rule = config["pomodoro"]["long_break_every_focus_sessions"]
    if completed_focus_sessions == 0 or completed_focus_sessions % rule != 0:
        return {}

    activities = config["long_break_self_care"]["activities"]
    strategy = config["long_break_self_care"]["selection_strategy"]
    if strategy == "cycle":
        index = (completed_focus_sessions // rule - 1) % len(activities)
        selected = activities[index]
    else:
        selected = random.choice(activities)

    encouragement = config["long_break_self_care"]["encouragement"]
    if encouragement["enabled"] and encouragement["phrases"]:
        selected = dict(selected)
        selected["message"] = f"{selected['message']} {random.choice(encouragement['phrases'])}"
    return selected
