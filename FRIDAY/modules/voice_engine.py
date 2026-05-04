import os
import sys
import tempfile
import requests

sys.path.append(os.path.expanduser("~") + "/FRIDAY")
from config import ELEVEN_KEY

ELEVEN_VOICE_ID = "pNInz6obpgDQGcFmaJgB"

def speak(text):
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
        headers = {
            "xi-api-key": ELEVEN_KEY,
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
            print(f"ElevenLabs error: {response.status_code}")
            fallback_speak(text)
    except Exception as e:
        print(f"Voice error: {e}")
        fallback_speak(text)

def fallback_speak(text):
    clean = text.replace('"', '').replace("'", "")
    os.system(f'espeak -s 150 -v en "{clean}" 2>/dev/null')

def listen_whisper():
    try:
        import whisper
        import sounddevice as sd
        import soundfile as sf
        import numpy as np

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
        return input("\nYou: ").lower()
    except:
        return ""