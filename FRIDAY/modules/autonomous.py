import threading
import time
import os
import sys
import psutil
import datetime

sys.path.append(os.path.expanduser("~") + "/FRIDAY/modules")

# ── BATTERY GUARD ─────────────────────────────────────
def battery_guard(say_func):
    def monitor():
        warned_low = False
        warned_critical = False
        while True:
            try:
                b = psutil.sensors_battery()
                if b:
                    percent = b.percent
                    plugged = b.power_plugged

                    if percent <= 10 and not plugged and not warned_critical:
                        say_func("Warning sir. Battery critically low at 10 percent. Please charge immediately.")
                        warned_critical = True
                        warned_low = True

                    elif percent <= 20 and not plugged and not warned_low:
                        say_func(f"Sir battery is low at {int(percent)} percent. Please connect charger.")
                        warned_low = True

                    elif percent > 25:
                        warned_low = False
                        warned_critical = False

                    elif plugged and percent >= 95:
                        say_func("Sir battery fully charged. You can unplug charger.")

            except Exception as e:
                print(f"Battery guard error: {e}")
            time.sleep(120)

    t = threading.Thread(target=monitor, daemon=True)
    t.start()
    print("Battery guard started")

# ── CPU/RAM MONITOR ───────────────────────────────────
def system_monitor(say_func):
    def monitor():
        while True:
            try:
                cpu = psutil.cpu_percent(interval=2)
                ram = psutil.virtual_memory().percent

                if cpu > 90:
                    say_func(f"Warning sir. CPU usage is very high at {int(cpu)} percent.")
                    time.sleep(60)

                if ram > 90:
                    say_func(f"Warning sir. RAM usage is very high at {int(ram)} percent.")
                    time.sleep(60)

            except Exception as e:
                print(f"System monitor error: {e}")
            time.sleep(60)

    t = threading.Thread(target=monitor, daemon=True)
    t.start()
    print("System monitor started")

# ── IDLE DETECTION ────────────────────────────────────
def idle_detection(say_func):
    def monitor():
        last_pos = None
        idle_time = 0
        warned = False

        while True:
            try:
                import pyautogui
                current_pos = pyautogui.position()

                if current_pos == last_pos:
                    idle_time += 1
                else:
                    idle_time = 0
                    warned = False

                last_pos = current_pos

                # 30 minutes idle = 360 checks x 5 seconds
                if idle_time >= 360 and not warned:
                    say_func("Sir you have been idle for 30 minutes. Should I lock the screen?")
                    warned = True

            except Exception as e:
                print(f"Idle detection error: {e}")
            time.sleep(5)

    t = threading.Thread(target=monitor, daemon=True)
    t.start()
    print("Idle detection started")

# ── MORNING BRIEFING AUTO ─────────────────────────────
def auto_morning_briefing(say_func):
    def monitor():
        briefing_done_today = None
        while True:
            try:
                now = datetime.datetime.now()
                today = now.date()

                if (now.hour == 8 and
                    now.minute < 5 and
                    briefing_done_today != today):

                    briefing_done_today = today
                    say_func("Good morning Prantick. Starting your daily briefing.")

                    try:
                        import requests
                        r = requests.get("https://wttr.in/Kolkata?format=3", timeout=5)
                        say_func(f"Weather update. {r.text}")
                    except:
                        pass

                    try:
                        import requests
                        import xml.etree.ElementTree as ET
                        r = requests.get("https://feeds.bbci.co.uk/news/rss.xml", timeout=5)
                        root = ET.fromstring(r.content)
                        items = root.findall('.//item/title')[:3]
                        say_func("Top news headlines.")
                        for item in items:
                            say_func(item.text)
                    except:
                        pass

                    say_func("Morning briefing complete. Have a great day sir.")

            except Exception as e:
                print(f"Morning briefing error: {e}")
            time.sleep(60)

    t = threading.Thread(target=monitor, daemon=True)
    t.start()
    print("Auto morning briefing started")

# ── SCREEN LOGGER ─────────────────────────────────────
def screen_logger():
    def logger():
        while True:
            try:
                now = datetime.datetime.now()
                if now.minute % 120 == 0:
                    path = os.path.expanduser("~") + f"/FRIDAY/outputs/auto_screenshot_{now.strftime('%Y%m%d_%H%M')}.png"
                    os.system(f"scrot '{path}'")
                    print(f"Auto screenshot saved: {path}")
            except Exception as e:
                print(f"Screen logger error: {e}")
            time.sleep(60)

    t = threading.Thread(target=logger, daemon=True)
    t.start()
    print("Screen logger started")

# ── START ALL ─────────────────────────────────────────
def start_all_autonomous(say_func):
    battery_guard(say_func)
    system_monitor(say_func)
    # idle_detection disabled — causes screen blink
    auto_morning_briefing(say_func)
    screen_logger()
    print("All autonomous systems started")