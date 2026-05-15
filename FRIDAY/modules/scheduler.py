import threading
import time
import datetime
import os
import sys

sys.path.append(os.path.expanduser("~") + "/FRIDAY/modules")

scheduled_tasks = []

def add_schedule(task_name, hour, minute, func):
    scheduled_tasks.append({
        "name": task_name,
        "hour": hour,
        "minute": minute,
        "func": func,
        "last_run": None
    })

def run_scheduler(say_func):
    def scheduler_loop():
        while True:
            now = datetime.datetime.now()
            for task in scheduled_tasks:
                if (now.hour == task["hour"] and
                    now.minute == task["minute"]):
                    last = task["last_run"]
                    if last is None or (now - last).seconds > 60:
                        task["last_run"] = now
                        try:
                            task["func"]()
                        except Exception as e:
                            print(f"Scheduler error: {e}")
            time.sleep(30)

    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()
    print("Scheduler started")

def add_voice_schedule(command, say_func):
    try:
        import re
        hour = 8
        minute = 0
        task_name = "custom task"

        numbers = re.findall(r'\d+', command)
        if len(numbers) >= 2:
            hour = int(numbers[0])
            minute = int(numbers[1])
        elif len(numbers) == 1:
            hour = int(numbers[0])
            minute = 0

        if "pm" in command and hour < 12:
            hour += 12
        if "am" in command and hour == 12:
            hour = 0

        for word in ["remind", "every", "day", "at", "am", "pm",
                     "to", "me", "schedule"]:
            command = command.replace(word, "")
        task_name = command.strip()

        def task_func():
            say_func(f"Scheduled reminder sir. {task_name}")

        add_schedule(task_name, hour, minute, task_func)

        import json
        schedules_file = os.path.expanduser("~") + "/FRIDAY/memory/schedules.json"
        schedules = []
        if os.path.exists(schedules_file):
            with open(schedules_file, 'r') as f:
                schedules = json.load(f)
        schedules.append({
            "name": task_name,
            "hour": hour,
            "minute": minute
        })
        with open(schedules_file, 'w') as f:
            json.dump(schedules, f, indent=2)

        return f"Scheduled {task_name} at {hour}:{minute:02d}"

    except Exception as e:
        return f"Schedule error: {e}"

def load_saved_schedules(say_func):
    try:
        import json
        schedules_file = os.path.expanduser("~") + "/FRIDAY/memory/schedules.json"
        if os.path.exists(schedules_file):
            with open(schedules_file, 'r') as f:
                schedules = json.load(f)
            for s in schedules:
                def make_func(name):
                    def f():
                        say_func(f"Scheduled reminder sir. {name}")
                    return f
                add_schedule(s["name"], s["hour"], s["minute"],
                           make_func(s["name"]))
            print(f"Loaded {len(schedules)} saved schedules")
    except Exception as e:
        print(f"Load schedules error: {e}")