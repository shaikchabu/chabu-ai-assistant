import os
import json
from datetime import datetime

def get_log_path():
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, "chat_history.json")

def get_status_path():
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, "status.json")

def save_chat(user_msg, ai_msg):
    log_path = get_log_path()
    history = []
    if os.path.exists(log_path):
        try:
            with open(log_path, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            pass
            
    history.append({
        "time": datetime.now().isoformat(),
        "user": user_msg,
        "assistant": ai_msg
    })
    
    with open(log_path, "w") as f:
        json.dump(history, f, indent=4)

def set_status(status_text, is_awake=False):
    """Saves the current status (Listening, Speaking, etc.) for the GUI."""
    status_path = get_status_path()
    with open(status_path, "w") as f:
        json.dump({"status": status_text, "is_awake": is_awake, "last_updated": str(os.times())}, f)

def get_status():
    """Reads the current status for the GUI."""
    status_path = get_status_path()
    if not os.path.exists(status_path):
        return {"status": "Standing By", "is_awake": False}
    try:
        with open(status_path, "r") as f:
            return json.load(f)
    except:
        return {"status": "Standing By", "is_awake": False}

def get_recent_history(limit=5):
    log_path = get_log_path()
    if not os.path.exists(log_path):
        return []
    
    try:
        with open(log_path, "r") as f:
            history = json.load(f)
    except:
        return []
        
    recent = history[-limit:]
    formatted_history = []
    for entry in recent:
        formatted_history.append(("user", entry.get("user", "")))
        formatted_history.append(("assistant", entry.get("assistant", "")))
        
    return formatted_history