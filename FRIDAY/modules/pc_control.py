import os
import sys
import subprocess
import pyautogui
import time

# Safety — stop if mouse hits corner
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# ── MOUSE CONTROL ─────────────────────────────────────
def mouse_click(x=None, y=None, button='left'):
    try:
        if x and y:
            pyautogui.click(x, y, button=button)
        else:
            pyautogui.click(button=button)
        return "Clicked"
    except Exception as e:
        return f"Click error: {e}"

def mouse_move(x, y):
    try:
        pyautogui.moveTo(x, y, duration=0.5)
        return f"Moved to {x} {y}"
    except Exception as e:
        return f"Move error: {e}"

def mouse_scroll(direction, amount=3):
    try:
        if direction == "up":
            pyautogui.scroll(amount)
        else:
            pyautogui.scroll(-amount)
        return f"Scrolled {direction}"
    except Exception as e:
        return f"Scroll error: {e}"

def get_mouse_position():
    x, y = pyautogui.position()
    return f"Mouse at {x} {y}"

def double_click(x=None, y=None):
    try:
        if x and y:
            pyautogui.doubleClick(x, y)
        else:
            pyautogui.doubleClick()
        return "Double clicked"
    except Exception as e:
        return f"Error: {e}"

def right_click(x=None, y=None):
    try:
        if x and y:
            pyautogui.rightClick(x, y)
        else:
            pyautogui.rightClick()
        return "Right clicked"
    except Exception as e:
        return f"Error: {e}"

# ── KEYBOARD CONTROL ──────────────────────────────────
def type_text(text):
    try:
        pyautogui.typewrite(text, interval=0.05)
        return f"Typed: {text}"
    except Exception as e:
        return f"Type error: {e}"

def press_key(key):
    try:
        pyautogui.press(key)
        return f"Pressed {key}"
    except Exception as e:
        return f"Key error: {e}"

def hotkey(*keys):
    try:
        pyautogui.hotkey(*keys)
        return f"Hotkey {keys}"
    except Exception as e:
        return f"Hotkey error: {e}"

def copy_text():
    hotkey('ctrl', 'c')
    time.sleep(0.3)
    try:
        import pyperclip
        return pyperclip.paste()
    except:
        return "Copied"

def paste_text():
    hotkey('ctrl', 'v')
    return "Pasted"

def select_all():
    hotkey('ctrl', 'a')
    return "Selected all"

def undo():
    hotkey('ctrl', 'z')
    return "Undone"

def save_file():
    hotkey('ctrl', 's')
    return "Saved"

def close_window():
    hotkey('alt', 'F4')
    return "Window closed"

def switch_window():
    hotkey('alt', 'tab')
    return "Switched window"

def minimize_window():
    hotkey('super', 'd')
    return "Minimized"

# ── SCREENSHOT + SCREEN READING ───────────────────────
def take_screenshot(filename=None):
    try:
        if not filename:
            import datetime
            filename = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
        path = os.path.expanduser("~") + f"/FRIDAY/outputs/{filename}"
        os.system(f"scrot '{path}'")
        return path
    except Exception as e:
        return f"Screenshot error: {e}"

def read_screen_text():
    try:
        import pytesseract
        from PIL import Image
        path = take_screenshot("temp_screen.png")
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        os.remove(path)
        return text[:500] if text else "No text found on screen"
    except Exception as e:
        return f"Screen read error: {e}"

def read_image_text(image_path):
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text if text else "No text found"
    except Exception as e:
        return f"Image read error: {e}"

# ── RUNNING APPS ──────────────────────────────────────
def get_running_apps():
    try:
        result = subprocess.run(
            ['wmctrl', '-l'],
            capture_output=True, text=True
        )
        if result.stdout:
            apps = []
            for line in result.stdout.strip().split('\n'):
                parts = line.split(None, 3)
                if len(parts) >= 4:
                    apps.append(parts[3])
            return apps[:10]
        return ["Could not get running apps"]
    except:
        result = subprocess.run(
            ['ps', 'aux', '--no-headers'],
            capture_output=True, text=True
        )
        apps = []
        for line in result.stdout.split('\n')[:10]:
            parts = line.split()
            if parts:
                apps.append(parts[-1])
        return apps

def kill_process(name):
    try:
        os.system(f"pkill -f {name}")
        return f"Killed {name}"
    except Exception as e:
        return f"Kill error: {e}"

def get_system_processes():
    try:
        import psutil
        procs = []
        for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                if p.info['cpu_percent'] > 1:
                    procs.append(
                        f"{p.info['name']} CPU:{p.info['cpu_percent']}%"
                    )
            except:
                pass
        return procs[:5] if procs else ["No high CPU processes"]
    except Exception as e:
        return [f"Error: {e}"]

# ── FILE SYSTEM FULL CONTROL ──────────────────────────
def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
        return f"Folder created at {path}"
    except Exception as e:
        return f"Folder error: {e}"

def delete_folder(path):
    try:
        import shutil
        shutil.rmtree(path)
        return f"Deleted {path}"
    except Exception as e:
        return f"Delete error: {e}"

def move_file(src, dst):
    try:
        import shutil
        shutil.move(src, dst)
        return f"Moved to {dst}"
    except Exception as e:
        return f"Move error: {e}"

def copy_file(src, dst):
    try:
        import shutil
        shutil.copy2(src, dst)
        return f"Copied to {dst}"
    except Exception as e:
        return f"Copy error: {e}"

def list_directory(path=None):
    try:
        if not path:
            path = os.path.expanduser("~")
        items = os.listdir(path)
        return items[:15]
    except Exception as e:
        return [f"Error: {e}"]

def get_file_info(path):
    try:
        stat = os.stat(path)
        size = stat.st_size
        return f"Size: {size} bytes"
    except Exception as e:
        return f"Error: {e}"

# ── RUN PYTHON FILES ──────────────────────────────────
def run_python(filepath):
    try:
        result = subprocess.run(
            ['python3', filepath],
            capture_output=True,
            text=True,
            timeout=30
        )
        out = result.stdout[:200] if result.stdout else result.stderr[:200]
        return f"Done. Output: {out}"
    except subprocess.TimeoutExpired:
        return "Program timed out after 30 seconds"
    except Exception as e:
        return f"Run error: {e}"

def run_terminal_command(cmd):
    try:
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        out = result.stdout[:200] if result.stdout else result.stderr[:200]
        return out if out else "Command done"
    except Exception as e:
        return f"Command error: {e}"