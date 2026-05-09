import pywhatkit
import datetime
import os
import json

CONTACTS_FILE = os.path.expanduser("~") + "/FRIDAY/memory/contacts.json"

def load_contacts():
    try:
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_contact(name, phone):
    try:
        contacts = load_contacts()
        name = name.strip()
        phone = phone.strip()
        if not phone.startswith("+"):
            phone = "+" + phone
        contacts[name.lower()] = phone
        contacts[name] = phone
        os.makedirs(os.path.dirname(CONTACTS_FILE), exist_ok=True)
        with open(CONTACTS_FILE, 'w') as f:
            json.dump(contacts, f, indent=2)
        print(f"Contact saved: {name} = {phone}")
        return f"Contact {name} saved with number {phone}"
    except Exception as e:
        print(f"Save error: {e}")
        return f"Could not save contact: {e}"
    
def send_whatsapp_to_contact(name, message):
    contacts = load_contacts()
    # try multiple ways to find contact
    name_lower = name.lower().strip()
    phone = None
    for key in contacts:
        if key.lower().strip() == name_lower:
            phone = contacts[key]
            break
    if phone:
        return send_whatsapp(phone, message)
    else:
        print(f"Available contacts: {list(contacts.keys())}")
        return f"Contact {name} not found. Say save contact to add."

def send_whatsapp(phone, message, wait_time=15):
    try:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute + 2
        if minute >= 60:
            minute = minute - 60
            hour = hour + 1
        pywhatkit.sendwhatmsg(
            phone_no=phone,
            message=message,
            time_hour=hour,
            time_min=minute,
            wait_time=wait_time,
            tab_close=True
        )
        return f"WhatsApp message sent"
    except Exception as e:
        return f"WhatsApp error: {e}"