import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.expanduser("~") + "/FRIDAY")
from config import GEMINI_KEY

MEMORY_FILE = os.path.expanduser("~") + "/FRIDAY/memory/conversation.json"

def load_history():
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_history(history):
    try:
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        with open(MEMORY_FILE, 'w') as f:
            json.dump(history[-50:], f, indent=2)
    except Exception as e:
        print(f"Memory save error: {e}")

def ai_chat(question):
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        history = load_history()
        history_text = ""
        for h in history[-10:]:
            role = "User" if h["role"] == "user" else "FRIDAY"
            history_text += f"{role}: {h['content']}\n"

        full_prompt = f"""You are FRIDAY, an advanced AI assistant like Iron Man's AI.
Smart, helpful, professional, slightly witty.
Keep answers SHORT — max 3 sentences for voice.
Current time: {datetime.now().strftime("%B %d %Y, %I:%M %p")}

Previous conversation:
{history_text}

User: {question}
FRIDAY:"""

        response = model.generate_content(full_prompt)
        answer = response.text.strip()

        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        save_history(history)
        return answer

    except Exception as e:
        return f"AI error: {e}"

def write_code(instruction):
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Write complete Python code for: {instruction}\nReturn ONLY raw code. No explanation. No markdown. No backticks."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"# Error: {e}"

def clear_memory():
    try:
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        return "Memory cleared"
    except:
        return "Could not clear memory"