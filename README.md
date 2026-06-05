HEAD
# Chabu AI — Hackathon Edition

**Voice-controlled desktop AI assistant** with a live Mission Control dashboard.  
Wake word: **"harry potter"** (say it in the CLI, then give your command).

## One-line pitch

> Chabu lets you run your PC with your voice — open apps, manage notes & tasks, and talk to Gemini — while a real-time dashboard shows everything happening.

## Quick start (judges / demo)

1. Install [Python 3.12+](https://www.python.org/downloads/)
2. Open this folder in terminal
3. Create `.env` in project root:
   ```
   GEMINI_API_KEY=your_google_ai_studio_key
   ```
4. Run:
   ```bat
   start_chabu.bat
   ```
5. **Terminal** — wait for *Standing by…*, say **"harry potter"**, then *"hello"* or *"open google"*
6. **Browser** — open http://localhost:8501 for Mission Control

## Features (demo checklist)

| Feature | Voice example | Web dashboard |
|--------|----------------|---------------|
| Wake / sleep | Say `harry potter` | Status: AWAKE / STANDBY |
| AI chat | Any question | Neural Terminal tab |
| Notes | `remember buy milk` | Productivity → add note |
| Tasks | `add task finish slides` | Productivity → add / complete |
| Open apps | `open google`, `open linkedin` | Quick launch buttons |
| System | `check system`, `take a screenshot` | Voice only |
| Personality | `change personality to funny` | Sidebar → Save profile |

## Project structure

```
chabu-ai-assistant/
├── cli_assistant/     # Voice loop (mic + commands)
├── web_assistant/     # Streamlit Mission Control
├── shared/            # Notes, tasks, memory, logs
├── config.json        # Wake word, version, demo script
├── launcher.py        # Starts CLI + web together
└── start_chabu.bat    # Double-click to run
```

## Tech stack

- **Speech:** Google Speech Recognition + Windows SAPI5 TTS  
- **AI:** Google Gemini (`google-genai`)  
- **UI:** Streamlit + live auto-refresh  
- **OS:** Windows (win32com, pyautogui)

## Team

Chabu Labs — *Your Voice · Your Control*

# CHABU AI Assistant 🤖

CHABU AI Assistant is a Python-based intelligent personal assistant that supports voice commands, AI-powered conversations, reminders, task management, WhatsApp automation, and a modern Streamlit web dashboard.

## Features

* 🎤 Voice Command Recognition
* 🗣️ Text-to-Speech Responses
* 🤖 AI-Powered Conversations
* 📋 Notes & Task Management
* ⏰ Reminders & Scheduling
* 💬 WhatsApp Automation
* 🌐 Streamlit Web Dashboard
* 📊 Statistics & Logging
* ⚙️ Configurable Settings

## Tech Stack

* Python
* Streamlit
* SpeechRecognition
* Text-to-Speech (TTS)
* AI Integration
* JSON Data Storage

## Project Structure

* `cli_assistant/` – Voice assistant modules
* `web_assistant/` – Streamlit dashboard
* `shared/` – Shared utilities and data management
* `assets/` – Logos and UI assets

## Getting Started

```bash
pip install -r requirements.txt
python launcher.py
```

## License

This project is for learning, experimentation, and personal productivity purposes.
 f796c26008b264bb4b09f69d09a4adf03d8db7f5
