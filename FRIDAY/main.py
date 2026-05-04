import pyttsx3
import os
import subprocess
import psutil
import webbrowser
import datetime
import sys

sys.path.append(os.path.expanduser("~") + "/FRIDAY/modules")
sys.path.append(os.path.expanduser("~") + "/FRIDAY/memory")

# ── VOICE SETUP ──────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', 165)

def say(text):
    print(f"\nFRIDAY: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening... speak now")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=6)
            command = r.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("No speech heard")
            return ""
        except sr.UnknownValueError:
            print("Could not understand")
            return ""
        except Exception as e:
            print(f"Mic error: {e}")
            return ""

# ── SYSTEM COMMANDS ───────────────────────────────────
def open_app(name):
    apps = {
        "chrome":     ["google-chrome"],
        "firefox":    ["firefox"],
        "vscode":     ["code"],
        "terminal":   ["gnome-terminal"],
        "files":      ["nautilus"],
        "calculator": ["gnome-calculator"],
        "vlc":        ["vlc"],
    }
    if name in apps:
        subprocess.Popen(apps[name])
        say(f"Opening {name}")
    else:
        say(f"App {name} not in list")

def system_status():
    b = psutil.sensors_battery()
    r = psutil.virtual_memory()
    c = psutil.cpu_percent(interval=1)
    bat = f"Battery {int(b.percent)}%" if b else "No battery"
    say(f"{bat}. RAM {int(r.percent)}%. CPU {c}%")

def volume_control(action):
    if action == "up":
        os.system("amixer set Master 10%+")
        say("Volume up")
    elif action == "down":
        os.system("amixer set Master 10%-")
        say("Volume down")
    elif action == "mute":
        os.system("amixer set Master toggle")
        say("Mute toggled")

# ── COMMAND ROUTER ────────────────────────────────────
def process_command(command):

    if "open chrome" in command:        open_app("chrome")
    elif "open firefox" in command:     open_app("firefox")
    elif "open vscode" in command:      open_app("vscode")
    elif "open terminal" in command:    open_app("terminal")
    elif "open files" in command:       open_app("files")
    elif "open calculator" in command:  open_app("calculator")
    elif "open vlc" in command:         open_app("vlc")

    elif "battery" in command or "status" in command:
        system_status()

    elif "cpu" in command:
        c = psutil.cpu_percent(interval=1)
        say(f"CPU at {c} percent")

    elif "ram" in command or "memory" in command:
        r = psutil.virtual_memory()
        say(f"RAM usage {int(r.percent)} percent")

    elif "time" in command:
        t = datetime.datetime.now().strftime("%I:%M %p")
        say(f"Time is {t}")

    elif "date" in command:
        d = datetime.datetime.now().strftime("%B %d %Y")
        say(f"Today is {d}")

    elif "volume up" in command:        volume_control("up")
    elif "volume down" in command:      volume_control("down")
    elif "mute" in command:             volume_control("mute")

    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://google.com/search?q={query}")
        say(f"Searching {query}")

    elif "youtube" in command:
        query = command.replace("play", "").replace("youtube", "").strip()
        webbrowser.open(f"https://youtube.com/search?q={query}")
        say(f"Opening YouTube for {query}")

    elif "create file" in command:
        from file_manager import create_file, open_file
        name = command.replace("create file", "").strip()
        if not name:
            name = "new_file.txt"
        path = create_file(name)
        open_file(path)
        say(f"File {name} created")

    elif "find file" in command:
        from file_manager import find_file
        name = command.replace("find file", "").strip()
        results = find_file(name)
        if results:
            say(f"Found {len(results)} files. First at {results[0]}")
        else:
            say("File not found")

    elif "remember" in command and " is " in command:
        from memory import remember
        part = command.replace("remember", "").strip()
        k, v = part.split(" is ", 1)
        remember(k.strip(), v.strip())
        say(f"Got it. Remembered {k}")

    elif "recall" in command:
        from memory import recall
        key = command.replace("recall", "").strip()
        val = recall(key)
        say(val if val else f"No memory of {key}")

    elif "write ml" in command:
        from ml_writer import write_ml_program
        task = command.replace("write ml", "").strip()
        say(f"Writing ML code for {task}")
        write_ml_program(task)
        say("Done. File opened.")

    elif "write code" in command:
        from ai_chat import write_code
        from file_manager import create_file, open_file
        task = command.replace("write code", "").strip()
        say(f"Writing code for {task}")
        code = write_code(task)
        path = create_file("friday_code.py", code)
        open_file(path)
        say("Code written and opened")

    elif "shutdown" in command:
        say("Shutting down")
        os.system("shutdown now")

    elif "restart" in command:
        say("Restarting")
        os.system("reboot")

    elif "stop" in command or "exit" in command or "goodbye" in command:
        say("FRIDAY going offline. Goodbye.")
        exit()

    else:
        from ai_chat import ai_chat
        answer = ai_chat(command)
        say(answer)

# ── START ─────────────────────────────────────────────
if __name__ == "__main__":
    say("FRIDAY online. All systems ready.")
    while True:
        cmd = listen()
        if cmd:
            process_command(cmd)