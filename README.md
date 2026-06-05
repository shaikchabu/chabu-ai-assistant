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
