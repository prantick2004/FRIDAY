import os
import sys
import tempfile

sys.path.append(os.path.expanduser("~") + "/FRIDAY")

def speak(text):
    try:
        from gtts import gTTS
        import pygame
        clean = text.strip()
        tts = gTTS(text=clean, lang='en', slow=False)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        tmp.close()
        pygame.mixer.init()
        pygame.mixer.music.load(tmp.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.unlink(tmp.name)
    except Exception as e:
        print(f"Voice error: {e}")
        clean = text.replace('"','').replace("'","")
        os.system(f'espeak -s 150 -v en "{clean}" 2>/dev/null')

def listen_whisper():
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("\nListening... speak now")
            r.energy_threshold = 300
            r.dynamic_energy_threshold = False
            r.adjust_for_ambient_noise(source, duration=0.2)
            try:
                audio = r.listen(source, timeout=8, phrase_time_limit=5)
                command = r.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                print(f"Error: {e}")
                return ""
    except Exception as e:
        print(f"Mic error: {e}")
        return input("\nYou: ").lower()