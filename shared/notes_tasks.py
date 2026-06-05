import os
import json

def get_data_path():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "shared"))
    return os.path.join(data_dir, "userdata.json")

def _load_data():
    path = get_data_path()
    if not os.path.exists(path):
        return {"notes": [], "tasks": []}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {"notes": [], "tasks": []}

def _save_data(data):
    path = get_data_path()
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# --- NOTES ---
def add_note(note_text):
    data = _load_data()
    data["notes"].append(note_text)
    _save_data(data)
    return f"Saved note: {note_text}"

def get_notes():
    data = _load_data()
    return data["notes"]

def delete_note(index):
    data = _load_data()
    if 0 <= index < len(data["notes"]):
        removed = data["notes"].pop(index)
        _save_data(data)
        return f"Deleted note: {removed}"
    return "Invalid note index."

# --- TASKS ---
def add_task(task_text):
    data = _load_data()
    data["tasks"].append({"task": task_text, "completed": False})
    _save_data(data)
    return f"Task added: {task_text}"

def get_tasks():
    data = _load_data()
    return data["tasks"]

def complete_task(index):
    data = _load_data()
    if 0 <= index < len(data["tasks"]):
        data["tasks"][index]["completed"] = True
        _save_data(data)
        return f"Task completed: {data['tasks'][index]['task']}"
    return "Invalid task index."

def delete_task(index):
    data = _load_data()
    if 0 <= index < len(data["tasks"]):
        removed = data["tasks"].pop(index)
        _save_data(data)
        return f"Deleted task: {removed['task']}"
    return "Invalid task index."
