from __future__ import annotations

from datetime import datetime

from rich.console import Console
from rich.table import Table

from habits.models import DayPlan


console = Console()


def render_dashboard(plan: DayPlan) -> None:
    now = datetime.now().strftime("%H:%M")
    table = Table(title=f"Habits Dashboard ({plan.day.isoformat()})")
    table.add_column("Widget")
    table.add_column("Value")

    next_item = next((i for i in plan.items if i.status == "pending"), None)
    table.add_row("Current timer", now)
    table.add_row("Day progress", f"{sum(i.status == 'done' for i in plan.items)}/{len(plan.items)} done")
    table.add_row("Next activity", next_item.block.title if next_item else "None")
    table.add_row("Overdue / missed count", str(plan.missed_count))
    console.print(table)
    console.print("Keybindings (vim-like): [a]ck [s]nooze s[k]ip [h]/[l] panels")
