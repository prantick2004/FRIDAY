import os
import sys
import subprocess
import psutil
import webbrowser
import datetime

sys.path.append(os.path.expanduser("~") + "/FRIDAY/modules")
sys.path.append(os.path.expanduser("~") + "/FRIDAY/memory")

# ── VOICE SETUP ──────────────────────────────────────
def say(text):
    print(f"\nFRIDAY: {text}")
    try:
        from voice_engine import speak
        speak(text)
    except Exception as e:
        print(f"Voice error: {e}")
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
        engine.say(text)
        engine.runAndWait()

def listen():
    try:
        from voice_engine import listen_whisper
        return listen_whisper()
    except Exception as e:
        print(f"Listen error: {e}")
        return keyboard_listen()

def keyboard_listen():
    try:
        command = input("\nYou: ").lower()
        return command
    except:
        return ""

# ── APP CONTROL ───────────────────────────────────────
def open_app(name):
    apps = {
        "chrome":      ["google-chrome"],
        "firefox":     ["firefox"],
        "vscode":      ["code"],
        "terminal":    ["gnome-terminal"],
        "files":       ["nautilus"],
        "calculator":  ["gnome-calculator"],
        "settings":    ["gnome-control-center"],
        "vlc":         ["vlc"],
        "spotify":     ["spotify"],
        "discord":     ["discord"],
        "telegram":    ["telegram-desktop"],
    }
    if name in apps:
        subprocess.Popen(apps[name])
        say(f"Opening {name}")
    else:
        say(f"App {name} not found in list")

# ── SYSTEM CONTROL ────────────────────────────────────
def system_status():
    b = psutil.sensors_battery()
    r = psutil.virtual_memory()
    c = psutil.cpu_percent(interval=1)
    bat = f"Battery {int(b.percent)} percent" if b else "No battery detected"
    say(f"{bat}. RAM usage {int(r.percent)} percent. CPU at {c} percent")

def volume_control(action):
    if action == "up":
        os.system("amixer set Master 10%+")
        say("Volume increased")
    elif action == "down":
        os.system("amixer set Master 10%-")
        say("Volume decreased")
    elif action == "mute":
        os.system("amixer set Master toggle")
        say("Mute toggled")

def take_screenshot():
    path = os.path.expanduser("~") + f"/FRIDAY/outputs/screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
    os.system(f"scrot {path}")
    say(f"Screenshot saved")

def get_weather(city="Kolkata"):
    try:
        import requests
        url = f"https://wttr.in/{city}?format=3"
        r = requests.get(url, timeout=5)
        say(r.text)
    except:
        say("Could not get weather right now")

def get_news():
    try:
        import requests
        url = "https://feeds.bbci.co.uk/news/rss.xml"
        r = requests.get(url, timeout=5)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(r.content)
        items = root.findall('.//item/title')[:3]
        say("Top 3 news headlines:")
        for item in items:
            say(item.text)
    except:
        say("Could not get news right now")

def kill_app(name):
    os.system(f"pkill -f {name}")
    say(f"Killed {name}")

def run_python_file(filepath):
    try:
        result = subprocess.run(['python3', filepath],
                              capture_output=True, text=True, timeout=30)
        output = result.stdout[:200] if result.stdout else result.stderr[:200]
        say(f"Program done. {output}")
    except Exception as e:
        say(f"Error running file: {e}")

# ── COMMAND ROUTER ────────────────────────────────────
def process_command(command):

    # ── Apps ──
    if "open chrome" in command:           open_app("chrome")
    elif "open firefox" in command:        open_app("firefox")
    elif "open vscode" in command:         open_app("vscode")
    elif "open terminal" in command:       open_app("terminal")
    elif "open files" in command:          open_app("files")
    elif "open calculator" in command:     open_app("calculator")
    elif "open vlc" in command:            open_app("vlc")
    elif "open spotify" in command:        open_app("spotify")
    elif "open discord" in command:        open_app("discord")
    elif "open telegram" in command:       open_app("telegram")

    # ── System info ──
    elif "battery" in command or "system status" in command:
        system_status()

    elif "cpu" in command:
        c = psutil.cpu_percent(interval=1)
        say(f"CPU usage is {c} percent")

    elif "ram" in command or "memory" in command:
        r = psutil.virtual_memory()
        say(f"RAM usage is {int(r.percent)} percent")

    elif "time" in command:
        t = datetime.datetime.now().strftime("%I:%M %p")
        say(f"Time is {t}")

    elif "date" in command:
        d = datetime.datetime.now().strftime("%B %d %Y")
        say(f"Today is {d}")

    # ── Volume ──
    elif "volume up" in command:           volume_control("up")
    elif "volume down" in command:         volume_control("down")
    elif "mute" in command:                volume_control("mute")

    # ── Web ──
    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://google.com/search?q={query}")
        say(f"Searching {query} on Google")

    elif "youtube" in command:
        query = command.replace("play", "").replace("youtube", "").strip()
        webbrowser.open(f"https://youtube.com/search?q={query}")
        say(f"Opening YouTube for {query}")

    elif "weather" in command:
        get_weather("Kolkata")

    elif "news" in command:
        get_news()

    # ── Screenshot ──
    elif "screenshot" in command:
        take_screenshot()

    # ── Kill app ──
    elif "kill" in command or "close" in command:
        app = command.replace("kill", "").replace("close", "").strip()
        kill_app(app)

    # ── Files ──
    elif "create file" in command:
        from file_manager import create_file, open_file
        name = command.replace("create file", "").strip()
        if not name:
            name = "new_file.txt"
        path = create_file(name)
        open_file(path)
        say(f"File {name} created and opened")

    elif "open file" in command:
        from file_manager import open_file
        name = command.replace("open file", "").strip()
        path = os.path.expanduser("~") + f"/FRIDAY/outputs/{name}"
        open_file(path)

    elif "find file" in command:
        from file_manager import find_file
        name = command.replace("find file", "").strip()
        results = find_file(name)
        if results:
            say(f"Found {len(results)} file. First one at {results[0]}")
        else:
            say("No file found with that name")

    # ── Memory ──
    elif "remember" in command and " is " in command:
        from memory import remember
        part = command.replace("remember", "").strip()
        k, v = part.split(" is ", 1)
        remember(k.strip(), v.strip())
        say(f"Got it. I will remember that {k} is {v}")

    elif "recall" in command:
        from memory import recall
        key = command.replace("recall", "").strip()
        val = recall(key)
        say(val if val else f"I have no memory of {key}")

    # ── Code writing ──
    elif "write ml" in command or "machine learning code" in command:
        from ml_writer import write_ml_program
        task = command.replace("write ml", "").replace("machine learning code", "").strip()
        if not task:
            say("Please tell me what ML task to write")
        else:
            say(f"Writing machine learning code for {task}. Please wait.")
            write_ml_program(task)
            say("Machine learning code written and opened")

    elif "write code" in command:
        from ai_chat import write_code
        from file_manager import create_file, open_file
        task = command.replace("write code", "").strip()
        say(f"Writing code for {task}. Please wait.")
        code = write_code(task)
        path = create_file("friday_code.py", code)
        open_file(path)
        say("Code written and opened in editor")

    elif "run file" in command:
        name = command.replace("run file", "").strip()
        path = os.path.expanduser("~") + f"/FRIDAY/outputs/{name}"
        run_python_file(path)

    # ── Power ──
    elif "shutdown" in command:
        say("Shutting down your computer. Goodbye.")
        os.system("shutdown now")

    elif "restart" in command:
        say("Restarting your computer.")
        os.system("reboot")

    elif "lock" in command:
        os.system("gnome-screensaver-command -l")
        say("Screen locked")

    # ── Exit FRIDAY ──
    elif "stop" in command or "exit" in command or "goodbye" in command or "offline" in command:
        say("FRIDAY going offline. Goodbye sir.")
        exit()

    # ── AI fallback for everything else ──
    else:
        from ai_chat import ai_chat
        say("Let me think about that.")
        answer = ai_chat(command)
        say(answer)

# ── MAIN START ────────────────────────────────────────
if __name__ == "__main__":
    say("FRIDAY online. All systems ready. How can I help you sir?")
    while True:
        cmd = listen()
        if cmd:
            process_command(cmd)