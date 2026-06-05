import json
import os
from datetime import datetime

from shared.logger import get_log_path
from shared.notes_tasks import get_notes, get_tasks


def get_dashboard_stats():
    """Metrics for hackathon demo dashboard."""
    history = []
    log_path = get_log_path()
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass

    today = datetime.now().date().isoformat()
    today_cmds = 0
    for entry in history:
        ts = entry.get("time", "")
        if ts.startswith(today) and entry.get("user"):
            today_cmds += 1

    tasks = get_tasks()
    notes = get_notes()
    done = sum(1 for t in tasks if t.get("completed"))

    return {
        "total_messages": len(history),
        "commands_today": today_cmds,
        "notes_count": len(notes),
        "tasks_total": len(tasks),
        "tasks_done": done,
        "tasks_pct": int((done / len(tasks)) * 100) if tasks else 0,
    }
