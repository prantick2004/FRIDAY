import os
import time
import webbrowser
import subprocess
import pyautogui

def send_whatsapp_by_name(name, message):
    try:
        # Step 1 - Open WhatsApp Web in existing tab
        subprocess.Popen(['google-chrome', '--new-tab', 'https://web.whatsapp.com'])
        time.sleep(8)  # Wait for WhatsApp to fully load

        # Step 2 - Make sure Chrome is focused
        pyautogui.hotkey('super', 'd')  # minimize all first
        time.sleep(0.5)
        pyautogui.hotkey('super', 'd')  # restore
        time.sleep(1)

        # Step 3 - Click search box in WhatsApp
        # Search box is at top left of WhatsApp Web
        pyautogui.hotkey('ctrl', 'alt', '/')
        time.sleep(2)

        # Step 4 - Clear search box first
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.press('delete')
        time.sleep(0.3)

        # Step 5 - Type contact name slowly
        for char in name:
            pyautogui.press(char)
            time.sleep(0.15)
        time.sleep(3)

        # Step 6 - Press Enter to open chat
        pyautogui.press('enter')
        time.sleep(2)

        # Step 7 - (Removed: Pressing enter above already focuses the message input box. Clicking risks losing focus)
        time.sleep(1)

        # Step 8 - Type message slowly
        for char in message:
            pyautogui.press(char)
            time.sleep(0.05)
        time.sleep(1)

        # Step 9 - Send
        pyautogui.press('enter')
        time.sleep(1)

        return f"Message sent to {name} successfully"

    except Exception as e:
        return f"WhatsApp error: {e}"

def save_contact(name, phone):
    import json
    CONTACTS_FILE = os.path.expanduser("~") + "/FRIDAY/memory/contacts.json"
    try:
        contacts = {}
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, 'r') as f:
                contacts = json.load(f)
        contacts[name.lower().strip()] = phone.strip()
        os.makedirs(os.path.dirname(CONTACTS_FILE), exist_ok=True)
        with open(CONTACTS_FILE, 'w') as f:
            json.dump(contacts, f, indent=2)
        return f"Contact {name} saved"
    except Exception as e:
        return f"Error: {e}"

def send_whatsapp_to_contact(name, message):
    return send_whatsapp_by_name(name, message)