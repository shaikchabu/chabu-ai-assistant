import os
import json
import threading
import time
from datetime import datetime
import win32com.client
import pythoncom

def get_reminders_path():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "shared"))
    return os.path.join(data_dir, "reminders.json")

def add_reminder(time_str, message):
    path = get_reminders_path()
    reminders = []
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                reminders = json.load(f)
        except:
            pass
            
    reminders.append({"time": time_str, "message": message, "done": False})
    
    with open(path, "w") as f:
        json.dump(reminders, f, indent=4)
    return f"Reminder set for {time_str}."

def check_reminders_thread():
    pythoncom.CoInitialize()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    path = get_reminders_path()
    
    while True:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    reminders = json.load(f)
                    
                current_time = datetime.now().strftime("%H:%M")
                updated = False
                
                for r in reminders:
                    if not r["done"] and r["time"] == current_time:
                        speaker.Speak(f"Reminder alert! {r['message']}", 1)
                        print(f"\n[REMINDER ALARM] {r['message']}")
                        r["done"] = True
                        updated = True
                        
                if updated:
                    with open(path, "w") as f:
                        json.dump(reminders, f, indent=4)
            except Exception as e:
                pass
                
        time.sleep(30)

def start_reminder_thread():
    t = threading.Thread(target=check_reminders_thread, daemon=True)
    t.start()
