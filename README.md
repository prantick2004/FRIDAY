# FRIDAY AI — Personal Intelligent Assistant

> *"Sometimes you gotta run before you can walk."* — Tony Stark

---

## What is FRIDAY?

FRIDAY is a fully voice-controlled personal AI assistant built entirely in Python, running locally on Ubuntu Linux. The name and concept are directly inspired by Tony Stark's AI from the Iron Man and Avengers films — an AI that doesn't just answer questions, but actually *does things* on your computer, manages your life, and works autonomously in the background.

This is not a simple chatbot. FRIDAY listens to your voice, understands your commands, and takes real action — opening applications, sending WhatsApp messages, reading your Gmail, controlling your mouse and keyboard, writing code, monitoring your system health, and much more. It runs 24/7 in the background and speaks back to you in a natural Google-quality voice.

I built this project from scratch over 7 days, adding new capabilities every single day. Every feature was tested, debugged, and refined until it worked properly.

---

## Why I Built This

I wanted to understand what it actually takes to build a real AI assistant — not just call an API and display text, but create something that has genuine control over a computer system. I also wanted something personal, something that felt like *my* assistant rather than a generic product.

The Iron Man FRIDAY concept was the perfect target. That AI opens systems, monitors everything, speaks naturally, remembers context, and acts autonomously. That became my goal.

---

## Features

### Voice Control
FRIDAY listens continuously using Google Speech Recognition. You speak naturally, it understands, and it responds in a clear Google TTS voice. No pressing buttons, no typing — just talk.

### Application Control
Open any application on your laptop by voice. Chrome, Firefox, VS Code, Terminal, Files, Calculator, VLC, Spotify, Discord, Telegram — all open instantly on command.

### Smart Website Opener
Open any website without pre-programming it. Say "open amazon.com" or "go to flipkart.com" and FRIDAY opens it. Popular sites like Gmail, YouTube, WhatsApp, Instagram, GitHub, Netflix all have dedicated shortcuts too.

### System Monitoring
Ask FRIDAY about battery percentage, CPU usage, RAM usage, time, date — it responds instantly. The autonomous system also watches these in the background and warns you automatically when battery drops below 20%, or when CPU/RAM usage spikes above 90%.

### Volume and System Control
Control system volume by voice — volume up, volume down, mute. Lock screen, shutdown, or restart your computer by voice.

### Full PC Mouse and Keyboard Control
FRIDAY can control your entire computer physically:
- Left click, right click, double click
- Scroll up and down
- Type any text by voice
- Copy, paste, undo, save
- Switch windows, minimize, close windows
- Press any keyboard key

### Screenshot and Screen Reading
Take a screenshot anytime by voice. FRIDAY also uses OCR (Tesseract) to read text visible on your screen and tell you what it says.

### Gmail Integration
FRIDAY connects to your Gmail account via the Google API. Read your unread emails by voice, search for emails by keyword, and send emails — all hands-free.

### Google Calendar
View today's events, check upcoming events for the next 7 days, and add new calendar events by voice.

### Reminder System
Set reminders that run in the background. FRIDAY checks every 30 seconds and speaks the reminder at the right time, even while you're doing something else.

### WhatsApp Messaging
Send WhatsApp messages to any contact entirely by voice. Say "send message to [name]", FRIDAY asks what to say, then automatically opens WhatsApp Web, finds the contact, types the message, and sends it — using intelligent browser automation.

### Spotify Control
Control Spotify playback by voice. Play specific songs, pause, resume, skip to next track, go to previous track, check what's currently playing, and set volume.

### AI Brain with Memory
FRIDAY is powered by Google Gemini AI (gemini-1.5-flash). Every conversation is saved to a local JSON memory file. FRIDAY remembers what you said in previous sessions and uses that context to give smarter, more personal answers. You can also explicitly save facts: "remember my birthday is June 5" and recall them later.

### Code Writing by Voice
Describe any program you want and FRIDAY writes the complete Python code, saves it to a file, and opens it in your editor — all by voice. This works for regular Python programs and also specifically for machine learning models.

### File System Control
Create files and folders, find files anywhere on your system, open files, and run Python scripts — all by voice.

### Morning Briefing
Every morning at 8 AM, FRIDAY automatically gives you a briefing without you asking:
- Good morning greeting
- Current time and date
- Live weather for your city
- Top 3 BBC news headlines
- Any pending reminders or calendar events

### Task Scheduler
Set recurring voice-activated schedules. "Schedule drink water every day at 9am" — FRIDAY saves it and runs it automatically every day. Schedules persist across restarts.

### Autonomous Background Systems
FRIDAY runs several monitoring threads silently in the background at all times:
- Battery guard (warns at 20% and 10%)
- CPU and RAM monitor (warns above 90%)
- Auto morning briefing at 8 AM
- Reminder checker every 30 seconds
- Automatic screenshot logger every 2 hours

### Face Recognition Login (Optional)
Register your face once by voice command. After that, FRIDAY uses your webcam to verify your identity on startup. If the face doesn't match, access is denied.

### GUI Dashboard
An Iron Man HUD-style dashboard built in tkinter shows live system status — time, date, CPU, RAM, battery — along with what FRIDAY is currently saying and quick-tap command buttons.

### Auto Start on Boot
FRIDAY is configured as a system service that launches automatically when Ubuntu starts, so it's always ready without you needing to do anything.

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.8 |
| Voice Input | Google Speech Recognition |
| Voice Output | Google Text-to-Speech (gTTS) + pygame |
| AI Brain | Google Gemini 1.5 Flash API |
| Memory | SQLite + JSON files |
| Gmail & Calendar | Google API Python Client |
| WhatsApp | PyAutoGUI + Browser Automation |
| Spotify | Spotipy (Spotify Web API) |
| PC Control | PyAutoGUI + subprocess |
| Screen Reading | Tesseract OCR + Pillow |
| Face Recognition | OpenCV + face_recognition |
| GUI Dashboard | tkinter |
| Scheduler | Python threading |
| System Monitor | psutil |
| Auto Start | systemd service |

---

## Project Structure

```
FRIDAY/
├── main.py                  # Core brain — command router and main loop
├── config.py                # API keys (gitignored — never uploaded)
├── dashboard.py             # Iron Man HUD GUI
├── .gitignore
├── credentials.json         # Google OAuth (gitignored)
│
├── modules/
│   ├── ai_chat.py           # Gemini AI integration + conversation memory
│   ├── voice_engine.py      # Voice input and output
│   ├── file_manager.py      # File system operations
│   ├── ml_writer.py         # Machine learning code generator
│   ├── pc_control.py        # Mouse, keyboard, screen control
│   ├── gmail_control.py     # Gmail read/send/search
│   ├── calendar_control.py  # Google Calendar integration
│   ├── reminders.py         # Reminder system with background checker
│   ├── whatsapp_control.py  # WhatsApp Web automation
│   ├── spotify_control.py   # Spotify playback control
│   ├── briefing.py          # Morning briefing generator
│   ├── autonomous.py        # Background monitoring systems
│   ├── scheduler.py         # Task scheduler
│   └── face_auth.py         # Face recognition login
│
├── memory/
│   ├── memory.py            # SQLite memory database
│   ├── conversation.json    # AI conversation history
│   ├── contacts.json        # WhatsApp contacts
│   ├── reminders.json       # Saved reminders
│   └── schedules.json       # Saved schedules
│
└── outputs/
    ├── friday_code.py       # AI-generated code files
    └── screenshots/         # Auto-saved screenshots
```

---

## How to Set Up

### Requirements
- Ubuntu 20.04 or later
- Python 3.8+
- Google account (for Gmail and Calendar)
- Gemini API key (free at aistudio.google.com)
- Spotify account (optional, for music control)
- ElevenLabs account (optional, for premium voice)
- Working microphone

### Installation

**Step 1 — Clone the repository:**
```bash
git clone https://github.com/YOURUSERNAME/FRIDAY-AI.git
cd FRIDAY-AI
```

**Step 2 — Install system dependencies:**
```bash
sudo apt update
sudo apt install -y espeak portaudio19-dev python3-pip python3-dev
sudo apt install -y tesseract-ocr scrot xdotool wmctrl mpg123 ffmpeg
sudo apt install -y python3-tk cmake
```

**Step 3 — Install Python libraries:**
```bash
pip3 install SpeechRecognition pyttsx3 pyautogui psutil requests
pip3 install beautifulsoup4 plyer pyperclip wikipedia pyaudio
pip3 install google-generativeai google-auth google-auth-oauthlib
pip3 install google-auth-httplib2 google-api-python-client
pip3 install gtts pygame opencv-python pytesseract pillow
pip3 install spotipy pywhatkit face-recognition dlib
pip3 install openai-whisper sounddevice soundfile
```

**Step 4 — Create your config file:**

Create a file called `config.py` in the FRIDAY folder:
```python
GEMINI_KEY            = "your_gemini_api_key"
ELEVEN_KEY            = "your_elevenlabs_key"
SPOTIFY_CLIENT_ID     = "your_spotify_client_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"
SPOTIFY_REDIRECT_URI  = "http://localhost:8888/callback"
```

**Step 5 — Set up Google API credentials:**

Go to console.cloud.google.com, create a project, enable Gmail API and Google Calendar API, create OAuth credentials, download the JSON file, and save it as `credentials.json` in the FRIDAY folder.

**Step 6 — Run FRIDAY:**
```bash
python3 main.py
```

**Step 7 — Auto start on boot (optional):**
```bash
sudo nano /etc/systemd/system/friday.service
```
Add the service configuration with your username, then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable friday
```

---

## Voice Commands Reference

### Applications
| Command | Action |
|---|---|
| "open chrome" | Opens Google Chrome |
| "open vscode" | Opens VS Code |
| "open terminal" | Opens Terminal |
| "open files" | Opens File Manager |
| "open gmail" | Opens Gmail in browser |
| "open whatsapp" | Opens WhatsApp Web |
| "go to amazon.com" | Opens any website |

### System
| Command | Action |
|---|---|
| "battery" | Battery and system status |
| "cpu" | CPU usage |
| "ram" | RAM usage |
| "time" | Current time |
| "volume up / down" | Adjust volume |
| "screenshot" | Takes screenshot |
| "lock" | Locks screen |
| "shutdown" | Shuts down computer |

### AI and Information
| Command | Action |
|---|---|
| "search [topic]" | Google search |
| "weather" | Current weather |
| "news" | Top 3 headlines |
| "what is [anything]" | Gemini AI answers |
| "write code [description]" | Writes Python code |
| "write ml [task]" | Writes ML model code |

### Communication
| Command | Action |
|---|---|
| "check email" | Reads unread emails |
| "send email" | Sends an email |
| "send message to [name]" | WhatsApp message |
| "my schedule" | Today's calendar |
| "remind me [task]" | Sets reminder |

### PC Control
| Command | Action |
|---|---|
| "left click" | Mouse left click |
| "right click" | Mouse right click |
| "scroll up / down" | Page scroll |
| "type [text]" | Types text |
| "copy / paste" | Clipboard control |
| "switch window" | Alt+Tab |

### Memory
| Command | Action |
|---|---|
| "remember [key] is [value]" | Saves information |
| "recall [key]" | Recalls saved info |
| "clear memory" | Clears AI chat history |

---

## Development Journey

This project was built day by day over one week:

**Day 1** — Foundation. Voice input with Google Speech Recognition, voice output with espeak, basic app launcher, system info commands, web search.

**Day 2** — Intelligence. Integrated Gemini AI as the brain, added conversation memory that persists across sessions, built the morning briefing system with live weather and news.

**Day 3** — Communication. Connected Gmail API for reading and sending emails, Google Calendar for schedule management, built a background reminder system.

**Day 4** — Physical control. Full mouse and keyboard control using PyAutoGUI, screenshot capture, OCR screen reading, process management.

**Day 5** — More communication. WhatsApp Web automation using browser control, Spotify API integration, upgraded voice to Google TTS for natural sound.

**Day 6** — Autonomy. Background monitoring threads for battery, CPU, RAM. Daily auto-briefing at 8 AM. Voice-activated task scheduler. Auto start on Ubuntu boot using systemd.

**Day 7** — Polish. Iron Man HUD GUI dashboard, face recognition login system, final command cleanup.

---

## Challenges I Faced

**PyAudio installation** was broken on my Ubuntu version. Solved by installing system-level portaudio dependencies separately before pip install.

**ElevenLabs API** changed their free tier policy during the project — free accounts can no longer use library voices via API. Switched to gTTS which is completely free and sounds natural.

**WhatsApp automation** was the most complex challenge. The first attempt used `Ctrl+K` to open the WhatsApp search, but that shortcut actually opens Chrome's address bar instead. Fixed by using `Ctrl+Alt+/` which is WhatsApp Web's own search shortcut. Also had issues with mouse clicks hitting the taskbar instead of the message box — solved by removing the click entirely since WhatsApp auto-focuses the message box after opening a chat.

**pyttsx3 segmentation fault** — the library crashed with a segmentation fault when called multiple times in a loop. Replaced entirely with direct espeak system calls and later gTTS.

**Conversation memory** — early versions lost context between sessions. Solved by saving the full conversation history to a JSON file and loading it at the start of each AI request.

---

## Security Notes

- `config.py` is in `.gitignore` and never uploaded to GitHub
- `credentials.json` (Google OAuth) is also gitignored
- API keys are never hardcoded in any uploaded file
- Face recognition data is stored locally only
- All WhatsApp automation happens on your local browser — no credentials are stored

---

## What's Next

There are several features I plan to add in future updates:

- Selenium-based web automation for more reliable WhatsApp and Gmail control
- Local LLM support using Ollama so FRIDAY works completely offline
- Home automation integration via MQTT for smart home control
- Mobile companion app that connects to FRIDAY remotely
- Voice training to recognize only the owner's voice
- Natural language file search using embeddings

---

## Built By

**Prantick Maity**

This project started as a personal challenge — to build something real, not just follow a tutorial. Every bug that came up was a learning opportunity. Every feature that finally worked after hours of debugging felt like a genuine achievement.

If you want to build your own version, feel free to fork this repository. The code is organized so that each module works independently — you can use just the Gmail integration, or just the PC control, without needing the full system.

---

*FRIDAY is not perfect. But neither was Mark 1.*
