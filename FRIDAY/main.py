import os
import sys
import subprocess
import psutil
import webbrowser
import datetime

sys.path.append(os.path.expanduser("~") + "/FRIDAY/modules")
sys.path.append(os.path.expanduser("~") + "/FRIDAY/memory")

# ── VOICE ─────────────────────────────────────────────
def say(text):
    print(f"\nFRIDAY: {text}")
    clean = text.replace('"', '').replace("'", "")
    os.system(f'espeak -s 150 -v en "{clean}" 2>/dev/null')


def listen():
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("\nListening... speak now")
            r.energy_threshold = 300
            r.dynamic_energy_threshold = False
            r.adjust_for_ambient_noise(source, duration=0.2)
            try:
                audio = r.listen(source, timeout=8, phrase_time_limit=5)
                command = r.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                print(f"Error: {e}")
                return ""
    except Exception as e:
        print(f"Mic error: {e}")
        return input("\nYou: ").lower()

# ── APP CONTROL ───────────────────────────────────────
def open_app(name):
    apps = {
        "chrome":     ["google-chrome"],
        "firefox":    ["firefox"],
        "vscode":     ["code"],
        "terminal":   ["gnome-terminal"],
        "files":      ["nautilus"],
        "calculator": ["gnome-calculator"],
        "settings":   ["gnome-control-center"],
        "vlc":        ["vlc"],
        "spotify":    ["spotify"],
        "discord":    ["discord"],
        "telegram":   ["telegram-desktop"],
    }
    if name in apps:
        subprocess.Popen(apps[name])
        say(f"Opening {name}")
    else:
        say(f"App {name} not found")

# ── SYSTEM ────────────────────────────────────────────
def system_status():
    b = psutil.sensors_battery()
    r = psutil.virtual_memory()
    c = psutil.cpu_percent(interval=1)
    bat = f"Battery {int(b.percent)} percent" if b else "No battery"
    say(f"{bat}. RAM {int(r.percent)} percent. CPU {c} percent")

def volume_control(action):
    cmds = {
        "up":   "amixer set Master 10%+",
        "down": "amixer set Master 10%-",
        "mute": "amixer set Master toggle"
    }
    os.system(cmds[action])
    say(f"Volume {action}")

def take_screenshot():
    path = os.path.expanduser("~") + f"/FRIDAY/outputs/screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
    os.system(f"scrot {path}")
    say("Screenshot saved")

def get_weather():
    try:
        import requests
        r = requests.get("https://wttr.in/Kolkata?format=3", timeout=5)
        say(r.text)
    except:
        say("Could not get weather")

def get_news():
    try:
        import requests
        import xml.etree.ElementTree as ET
        r = requests.get("https://feeds.bbci.co.uk/news/rss.xml", timeout=5)
        root = ET.fromstring(r.content)
        items = root.findall('.//item/title')[:3]
        say("Top 3 headlines:")
        for item in items:
            say(item.text)
    except:
        say("Could not get news")

def kill_app(name):
    os.system(f"pkill -f {name}")
    say(f"Closed {name}")

def run_python_file(name):
    path = os.path.expanduser("~") + f"/FRIDAY/outputs/{name}"
    try:
        result = subprocess.run(['python3', path],
                                capture_output=True, text=True, timeout=30)
        out = result.stdout[:150] if result.stdout else result.stderr[:150]
        say(f"Done. {out}")
    except Exception as e:
        say(f"Error: {e}")

# ── COMMAND ROUTER ────────────────────────────────────
def process_command(command):

    # Apps
    if   "open chrome"      in command: open_app("chrome")
    elif "open firefox"     in command: open_app("firefox")
    elif "open vscode"      in command: open_app("vscode")
    elif "open terminal"    in command: open_app("terminal")
    elif "open files"       in command: open_app("files")
    elif "open calculator"  in command: open_app("calculator")
    elif "open vlc"         in command: open_app("vlc")
    elif "open spotify"     in command: open_app("spotify")
    elif "open discord"     in command: open_app("discord")
    elif "open telegram"    in command: open_app("telegram")
    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")
        say("Opening Gmail sir")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        say("Opening YouTube sir")

    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        say("Opening WhatsApp sir")

    elif "open instagram" in command:
        webbrowser.open("https://instagram.com")
        say("Opening Instagram sir")

    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        say("Opening Facebook sir")

    elif "open twitter" in command:
        webbrowser.open("https://twitter.com")
        say("Opening Twitter sir")

    elif "open github" in command:
        webbrowser.open("https://github.com")
        say("Opening GitHub sir")

    elif "open netflix" in command:
        webbrowser.open("https://netflix.com")
        say("Opening Netflix sir")

    elif "open" in command and "." in command:
        words = command.replace("open","").strip().split()
        for word in words:
            if "." in word:
                url = word if word.startswith("http") else "https://" + word
                webbrowser.open(url)
                say(f"Opening {word} sir")
                break

    elif "go to" in command:
        site = command.replace("go to","").strip()
        if not site.startswith("http"):
            site = "https://" + site
        webbrowser.open(site)
        say(f"Opening {site} sir")

    # System
    elif "battery" in command or "system status" in command:
        system_status()
    elif "cpu" in command:
        say(f"CPU at {psutil.cpu_percent(interval=1)} percent")
    elif "ram" in command or "memory" in command:
        say(f"RAM at {int(psutil.virtual_memory().percent)} percent")
    elif "time" in command:
        say(f"Time is {datetime.datetime.now().strftime('%I:%M %p')}")
    elif "date" in command:
        say(f"Today is {datetime.datetime.now().strftime('%B %d %Y')}")

    # Volume
    elif "volume up"   in command: volume_control("up")
    elif "volume down" in command: volume_control("down")
    elif "mute"        in command: volume_control("mute")

    # Web
    elif "search" in command:
        q = command.replace("search","").strip()
        webbrowser.open(f"https://google.com/search?q={q}")
        say(f"Searching {q}")
    elif "youtube" in command:
        q = command.replace("play","").replace("youtube","").strip()
        webbrowser.open(f"https://youtube.com/search?q={q}")
        say(f"Opening YouTube for {q}")

    # Info
    elif "weather"    in command: get_weather()
    elif "news"       in command: get_news()
    elif "screenshot" in command: take_screenshot()

    # Kill
    elif "kill" in command or "close" in command:
        app = command.replace("kill","").replace("close","").strip()
        kill_app(app)

    # Files
    elif "create file" in command:
        from file_manager import create_file, open_file
        name = command.replace("create file","").strip() or "new_file.txt"
        path = create_file(name)
        open_file(path)
        say(f"File {name} created")

    elif "find file" in command:
        from file_manager import find_file
        name = command.replace("find file","").strip()
        results = find_file(name)
        say(f"Found at {results[0]}" if results else "File not found")

    elif "run file" in command:
        name = command.replace("run file","").strip()
        run_python_file(name)

    # Memory
    elif "remember" in command and " is " in command:
        from memory import remember
        part = command.replace("remember","").strip()
        k, v = part.split(" is ", 1)
        remember(k.strip(), v.strip())
        say(f"Remembered. {k} is {v}")

    elif "recall" in command:
        from memory import recall
        key = command.replace("recall","").strip()
        val = recall(key)
        say(val if val else f"No memory of {key}")

    elif "clear memory" in command:
        from ai_chat import clear_memory
        clear_memory()
        say("Memory cleared sir")

    # Code
    elif "write ml" in command:
        from ml_writer import write_ml_program
        task = command.replace("write ml","").strip()
        say(f"Writing ML code for {task}")
        write_ml_program(task)
        say("Done. File opened.")

    elif "write code" in command:
        from ai_chat import write_code
        from file_manager import create_file, open_file
        task = command.replace("write code","").strip()
        say(f"Writing code for {task}")
        code = write_code(task)
        path = create_file("friday_code.py", code)
        open_file(path)
        say("Code written and opened")

    # Power
    elif "shutdown" in command:
        say("Shutting down. Goodbye sir.")
        os.system("shutdown now")
    elif "restart" in command:
        say("Restarting.")
        os.system("reboot")
    elif "lock" in command:
        os.system("gnome-screensaver-command -l")
        say("Screen locked")

    # Exit
    elif any(x in command for x in ["stop","exit","goodbye","offline"]):
        say("FRIDAY going offline. Goodbye sir.")
        exit()

        # Gmail
    elif "read email" in command or "check email" in command:
        say("Checking your emails sir.")
        from gmail_control import read_emails
        emails = read_emails(3)
        for e in emails:
            say(e)

    elif "search email" in command:
        query = command.replace("search email","").strip()
        say(f"Searching emails for {query}")
        from gmail_control import search_emails
        emails = search_emails(query)
        for e in emails:
            say(e)

    elif "send email" in command:
        say("Who should I send to? Type the email address.")
        to = input("To: ").strip()
        say("What is the subject?")
        subject = input("Subject: ").strip()
        say("What should I write?")
        body = input("Body: ").strip()
        from gmail_control import send_email
        result = send_email(to, subject, body)
        say(result)

    # Calendar
    elif "today events" in command or "my schedule" in command:
        say("Checking your schedule for today.")
        from calendar_control import get_todays_events
        events = get_todays_events()
        for e in events:
            say(e)

    elif "upcoming events" in command or "this week" in command:
        say("Checking upcoming events.")
        from calendar_control import get_upcoming_events
        events = get_upcoming_events(7)
        for e in events:
            say(e)

    elif "add event" in command:
        task = command.replace("add event","").strip()
        say("What date? Type in format 2026-05-10")
        date = input("Date: ").strip()
        say("What time? Type in format 14:00")
        time = input("Time: ").strip()
        from calendar_control import add_event
        result = add_event(task, date, time)
        say(result)

    # Reminders
    elif "remind me" in command:
        from reminders import add_reminder
        parts = command.replace("remind me","").strip()
        say("How many minutes from now?")
        mins = input("Minutes: ").strip()
        result = add_reminder(parts, int(mins))
        say(result)

    elif "my reminders" in command:
        from reminders import get_pending_reminders
        pending = get_pending_reminders()
        for p in pending:
            say(p)

    # Gemini AI fallback
    else:
        from ai_chat import ai_chat
        say("Let me think.")
        answer = ai_chat(command)
        say(answer)

# ── BRIEFING ──────────────────────────────────────────
def morning_briefing():
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    say(f"{greeting} sir. FRIDAY online.")
    say(f"Time is {now.strftime('%I:%M %p')}.")
    say(f"Today is {now.strftime('%B %d %Y')}.")
    get_weather()
    get_news()
    say("Briefing complete. Ready for your commands sir.")

# ── START ─────────────────────────────────────────────
if __name__ == "__main__":
    from reminders import check_reminders
    check_reminders(say)
    morning_briefing()
    while True:
        cmd = listen()
        if cmd:
            process_command(cmd)