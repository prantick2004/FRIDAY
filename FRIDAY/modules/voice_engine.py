import os
import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
import tempfile
import subprocess

# ── ELEVENLABS SPEAK ─────────────────────────────────
ELEVEN_API_KEY = "sk_8bf168b0a948e9f85668e97cce73c3fc3d0ec6191d9b6bd9"
ELEVEN_VOICE_ID = "https://elevenlabs.io/app/api/voice-library?voiceId=NFG5qt843uXKj4pFvR7C"

def speak(text):
    try:
        import requests
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
        headers = {
            "xi-api-key": ELEVEN_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp.write(response.content)
            tmp.close()
            os.system(f"mpg123 -q {tmp.name}")
            os.unlink(tmp.name)
        else:
            fallback_speak(text)
    except Exception as e:
        print(f"ElevenLabs error: {e}")
        fallback_speak(text)

def fallback_speak(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    engine.say(text)
    engine.runAndWait()

# ── WHISPER LISTEN ────────────────────────────────────
def listen_whisper():
    try:
        import whisper
        print("\nListening... speak now")

        duration = 6
        sample_rate = 16000

        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='float32'
        )
        sd.wait()

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(tmp.name, audio_data, sample_rate)

        model = whisper.load_model("base")
        result = model.transcribe(tmp.name)
        os.unlink(tmp.name)

        command = result["text"].strip().lower()
        print(f"You said: {command}")
        return command

    except Exception as e:
        print(f"Whisper error: {e}")
        return keyboard_listen()

def keyboard_listen():
    try:
        command = input("\nYou: ").lower()
        return command
    except:
        return ""