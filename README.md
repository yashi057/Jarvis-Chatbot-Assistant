<div align="center">
<div align="center">
```
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
```
</div>

### Just A Rather Very Intelligent System
#### *An AI-powered desktop assistant — Iron Man style*

<br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Claude API](https://img.shields.io/badge/Claude_API-Sonnet_4-D97706?style=for-the-badge&logo=anthropic&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-00BFFF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)

<br/>

> **"Sometimes you gotta run before you can walk."** — Tony Stark

</div>

---

## 🧠 What is JARVIS?

JARVIS is a **voice-enabled AI desktop assistant** built in Python. You can talk to it, type to it, and it responds — both in text and out loud. For simple tasks like opening YouTube or checking the time, it handles it instantly. For everything else, it connects to **Anthropic's Claude AI** and gives you intelligent, context-aware answers.

Think of it as a personal command center that lives on your desktop.

---

## ✨ Features at a Glance

| Feature | Description |
|---|---|
| 🧠 Claude AI Brain | Powered by `claude-sonnet-4` for intelligent responses |
| 🎤 Voice Input | Speak commands using your microphone |
| 🔊 Text-to-Speech | Jarvis talks back using `pyttsx3` |
| 💬 Chat UI | Dark-mode interface with styled message bubbles |
| ⚡ Instant Commands | Time, date, search, open sites, jokes — no API call needed |
| 🔁 Memory | Maintains conversation context within a session |
| 🕐 Live Clock | Real-time clock and date in the sidebar |

---

## 🏗️ Architecture — How It Works

Here's the full flow from when you type/speak something to when Jarvis responds:

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│              (Keyboard typing  OR  Microphone)                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │      main.py        │  ← CustomTkinter UI
          │  (App + Chat UI)    │    handles layout, buttons,
          │                     │    chat bubbles, clock
          └──────┬──────┬───────┘
                 │      │
    ┌────────────▼─┐  ┌─▼──────────────┐
    │  voice.py    │  │  commands.py   │
    │              │  │                │
    │ • pyttsx3    │  │ Check if query │
    │   (speak)    │  │ matches a      │
    │ • SpeechRec  │  │ built-in rule  │
    │   (listen)   │  │                │
    └────────────┬─┘  └─┬──────────────┘
                 │       │
                 │    MATCH?
                 │    ├── ✅ YES → Return instant response
                 │    │           (time / open YouTube / etc.)
                 │    │
                 │    └── ❌ NO  → Fall back to Claude API
                 │                        │
                 │             ┌──────────▼──────────┐
                 │             │   api_client.py      │
                 │             │                      │
                 │             │ • Sends message to   │
                 │             │   Anthropic Claude   │
                 │             │ • Maintains history  │
                 │             │   (last 20 turns)    │
                 │             │ • Returns response   │
                 │             └──────────┬───────────┘
                 │                        │
                 │             ┌──────────▼───────────┐
                 │             │   Anthropic Cloud    │
                 │             │  claude-sonnet-4     │
                 │             │  (AI processing)     │
                 │             └──────────────────────┘
                 │
    ┌────────────▼──────────────────────────┐
    │           RESPONSE                    │
    │  • Displayed as chat bubble in UI     │
    │  • Spoken aloud via pyttsx3 (TTS)     │
    └───────────────────────────────────────┘
```

### The Smart Fallback System

The key design decision in this project is the **two-layer command system**:

1. `commands.py` checks the input first — if it's a simple task like `"open youtube"` or `"what time is it"`, it handles it locally in milliseconds with zero API cost.
2. If nothing matches, `api_client.py` fires a request to Claude with the full conversation history so Claude has context.

This means Jarvis is **fast for common tasks** and **smart for everything else**.

---

## 🛠️ Tech Stack

| Library | Version | Why We Used It |
|---|---|---|
| `customtkinter` | 5.2+ | Modern dark-mode UI widgets — regular `tkinter` looks outdated |
| `anthropic` | 0.34+ | Official Python SDK for Claude API — clean and well-documented |
| `pyttsx3` | 2.90+ | Offline text-to-speech — works without internet, no API key needed |
| `SpeechRecognition` | 3.10+ | Wraps Google Speech API for microphone input |
| `pyaudio` | 0.2.14+ | Low-level microphone access (required by SpeechRecognition) |
| `python-dotenv` | 1.0+ | Loads `.env` so your API key never touches your source code |

---

## 📁 Project Structure

```
jarvis-ai/
│
├── main.py                   # 🖥️  App entry point — UI layout & event handling
│
├── modules/
│   ├── __init__.py           #     Makes this a Python package
│   ├── voice.py              # 🎤  Text-to-speech + speech recognition
│   ├── commands.py           # ⚡  Built-in command handler (no API needed)
│   └── api_client.py         # 🧠  Claude API integration + chat history
│
├── .env                      # 🔑  YOUR API key (never commit this!)
├── .env.example              # 📋  Template — safe to share on GitHub
├── .gitignore                # 🚫  Tells Git what NOT to upload
├── requirements.txt          # 📦  All dependencies listed here
└── README.md                 # 📖  This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- A microphone (for voice input)
- An Anthropic API key — free at [console.anthropic.com](https://console.anthropic.com/settings/keys)

---

## 🗣️ Available Commands

### Built-in (instant, no API call)

| Say or Type | What Happens |
|---|---|
| `hello` / `hi` / `hey` | Greeting based on time of day |
| `what time is it` | Current time |
| `what's today's date` | Today's full date |
| `search machine learning` | Opens Google search in browser |
| `youtube search lofi music` | Opens YouTube search |
| `open youtube` | Opens YouTube |
| `open github` | Opens GitHub |
| `calculate 150 * 12` | Quick calculator |
| `tell me a joke` | Random programmer joke |
| `bye` / `exit` | Closes the app |

### Everything else → Claude AI

Anything not matched above is sent to Claude. Examples:

- *"Explain recursion in simple terms"*
- *"Write a Python function to reverse a string"*
- *"What's the capital of Kazakhstan?"*
- *"Summarise what we talked about"* ← it remembers the session!

---

## 🔧 Customise Jarvis

**Change the AI personality** — edit `SYSTEM_PROMPT` in `modules/api_client.py`:
```python
SYSTEM_PROMPT = """You are JARVIS... (edit this to change personality)"""
```

**Add a new command** — add an `if` block in `modules/commands.py`:
```python
if "open spotify" in q:
    webbrowser.open("https://open.spotify.com")
    return "Opening Spotify."
```

**Change voice speed** — edit `modules/voice.py`:
```python
_engine.setProperty("rate", 175)  # higher = faster
```

**Change AI model** — edit `modules/api_client.py`:
```python
model="claude-sonnet-4-20250514"  # swap to opus for smarter responses
```

---

## 💡 Ideas to Extend This Project

- 🌦️ Weather integration using OpenWeatherMap API
- 🎵 Spotify playback controls
- 📁 Open local files and folders by name
- 💾 Save chat history to a `.txt` or `.json` file
- ⚙️ Settings panel for voice speed, theme, and language

---


## 📄 License

MIT — build on it, break it, ship it. Leave a ⭐ if it helped!

---

<div align="center">
  <sub>Built with ❤️ and Python </sub>
</div>
