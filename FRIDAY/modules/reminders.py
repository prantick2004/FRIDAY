import os
import json
import datetime
import threading

REMINDERS_FILE = os.path.expanduser("~") + "/FRIDAY/memory/reminders.json"

def load_reminders():
    try:
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_reminders(reminders):
    os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)

def add_reminder(task, minutes):
    reminders = load_reminders()
    remind_time = (datetime.datetime.now() +
                   datetime.timedelta(minutes=minutes)).isoformat()
    reminders.append({
        "task": task,
        "time": remind_time,
        "done": False
    })
    save_reminders(reminders)
    return f"Reminder set for {task} in {minutes} minutes"

def check_reminders(say_func):
    def checker():
        while True:
            reminders = load_reminders()
            now = datetime.datetime.now()
            changed = False
            for r in reminders:
                if not r['done']:
                    remind_time = datetime.datetime.fromisoformat(r['time'])
                    if now >= remind_time:
                        say_func(f"Reminder sir. {r['task']}")
                        r['done'] = True
                        changed = True
            if changed:
                save_reminders(reminders)
            import time
            time.sleep(30)

    t = threading.Thread(target=checker, daemon=True)
    t.start()

def get_pending_reminders():
    reminders = load_reminders()
    pending = [r for r in reminders if not r['done']]
    if not pending:
        return ["No pending reminders"]
    return [f"{r['task']} at {r['time']}" for r in pending]