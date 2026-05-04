import google.generativeai as genai

genai.configure(api_key="AIzaSyDqYJGDDKjAWW5eX42NYGUB74EbbWS0zj0")
model = genai.GenerativeModel("gemini-1.5-flash")

conversation_history = [
    "You are FRIDAY, Iron Man's AI assistant. Be helpful, polite, and answer as if you are talking to a human."
]

def ai_chat(question):
    try:
        conversation_history.append(f"User: {question}")
        prompt = "\n".join(conversation_history) + "\nFRIDAY:"
        response = model.generate_content(prompt)
        answer = response.text.strip()
        conversation_history.append(f"FRIDAY: {answer}")
        return answer
    except Exception as e:
        return f"AI error: {e}"

def write_code(instruction):
    try:
        prompt = f"Write complete Python code for: {instruction}\nReturn ONLY raw code. No explanation. No markdown."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"# Error: {e}"