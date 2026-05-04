import requests
import datetime
import os
import sys

sys.path.append(os.path.expanduser("~") + "/FRIDAY/modules")

def get_weather():
    try:
        r = requests.get("https://wttr.in/Kolkata?format=3", timeout=5)
        return r.text.strip()
    except:
        return "Weather unavailable"

def get_news():
    try:
        import xml.etree.ElementTree as ET
        r = requests.get("https://feeds.bbci.co.uk/news/rss.xml", timeout=5)
        root = ET.fromstring(r.content)
        items = root.findall('.//item/title')[:3]
        return [item.text for item in items]
    except:
        return ["News unavailable"]

def morning_briefing(say_func):
    now = datetime.datetime.now()
    hour = now.hour

    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    say_func(f"{greeting} sir. FRIDAY online. All systems ready.")

    t = now.strftime("%I:%M %p")
    d = now.strftime("%B %d, %Y")
    say_func(f"It is {t} on {d}.")

    say_func("Checking weather in Kolkata.")
    weather = get_weather()
    say_func(f"{weather}")

    say_func("Top news headlines.")
    headlines = get_news()
    for i, h in enumerate(headlines, 1):
        say_func(f"Headline {i}. {h}")

    say_func("Briefing complete. How can I help you sir?")