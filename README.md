<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&size=13&duration=3000&pause=1000&color=00D4FF&center=true&vCenter=true&multiline=true&width=600&height=100&lines=%5B+INITIALIZING+J.A.R.V.I.S+MARK+VII+...+%5D;%5B+NEURAL+PATHWAYS%3A+ONLINE+%5D;%5B+ALL+SYSTEMS+NOMINAL.+WELCOME+BACK.+%5D" alt="Boot Sequence"/>

<br/>

```
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
```

### `// MARK VII — IRON MAN HUD EDITION`

*Just A Rather Very Intelligent System — now with a real HUD*

<br/>

![Python](https://img.shields.io/badge/PYTHON-3.10%2B-00d4ff?style=for-the-badge&logo=python&logoColor=00d4ff&labelColor=050a0f)
![Claude](https://img.shields.io/badge/CLAUDE-SONNET_4-ff6b1a?style=for-the-badge&logo=anthropic&logoColor=ff6b1a&labelColor=050a0f)
![tkinter](https://img.shields.io/badge/UI-TKINTER_HUD-00ff88?style=for-the-badge&logoColor=00ff88&labelColor=050a0f)
![License](https://img.shields.io/badge/LICENSE-MIT-00d4ff?style=for-the-badge&labelColor=050a0f)

<br/>

> *"Sometimes you gotta run before you can walk."*
> — Tony Stark

</div>

---

```
◈ ─────────────────────────────────────────────────── SYSTEM STATUS ── ◈
  VOICE ENGINE    ██████████  ONLINE
  SPEECH INPUT    ██████████  ONLINE
  CLAUDE API      ██████████  CONNECTED
  HUD INTERFACE   ██████████  ACTIVE
◈ ──────────────────────────────────────────────────────────────────── ◈
```

---

## `[ 01 ]` // WHAT IS THIS?

JARVIS is a **voice-enabled AI desktop assistant** with a full **Iron Man HUD interface** — animated rotating rings, live system diagnostics, a cinematic boot sequence, and Claude AI powering every conversation.

This isn't just a chatbot. It's a personal command center that looks like it belongs in Stark Tower.

---

## `[ 02 ]` // SCREENSHOTS

```
┌─────────────────────────────────────────────────────────────────────┐
│  ◈  JARVIS  //  MARK VII                              ◉ CLAUDE API  │
├────────────────────┬────────────────────────────────────────────────┤
│                    │  //  INITIALIZING J.A.R.V.I.S MARK VII ...     │
│    ╭──────────╮    │  //  ALL SYSTEMS NOMINAL. WELCOME BACK.        │
│   ╱  ◉  ◉  ◉  ╲   │                                                │
│  │   ───────   │   │  [22:41:05] JARVIS ▶▶                         │
│   ╲  ─  ◈  ─  ╱   │  ┃ Good evening. How can I assist you today?  │
│    ╰──────────╯    │                                                │
│                    │  [22:41:18] YOU ▶▶                            │
│  [ SYSTEM ONLINE ] │  ┃ Open YouTube                               │
│  MODE: STANDBY     │                                                │
│  ─────────────     │  [22:41:18] JARVIS ▶▶                         │
│  CPU  ████░░  42%  │  ┃ Opening YouTube for you, sir.              │
│  RAM  ██████  61%  │                                                │
│  PWR  ████████ 82% │  ─────────────────────────────────────────    │
│  ─────────────     │  ▶ INPUT: [________________] [🎤] [TRANSMIT]  │
│  22:41:24          │                                                │
│  SUNDAY 19 APR     │                                                │
└────────────────────┴────────────────────────────────────────────────┘
```

---

## `[ 03 ]` // FEATURES

```
  ◉  ANIMATED HUD RING      Rotating arcs that change color based on
                             Jarvis's current state — cyan (standby),
                             orange (thinking), green (listening)

  ◉  LIVE SYSTEM STATS      Real-time CPU, RAM, and battery bars
                             powered by psutil — updates every 1.5s

  ◉  BOOT SEQUENCE          Cinematic line-by-line startup animation
                             like a real system initializing

  ◉  CLAUDE AI BRAIN        Every unrecognised command goes to Claude
                             Sonnet with full conversation memory

  ◉  VOICE INPUT            Speak to Jarvis — Google Speech API
                             transcribes and processes your command

  ◉  TEXT-TO-SPEECH         Jarvis talks back — offline via pyttsx3,
                             no internet needed for voice output

  ◉  SMART FALLBACK         Built-in commands run instantly (no API),
                             everything else routes to Claude

  ◉  TIMESTAMPED LOGS       Every message tagged [HH:MM:SS] — looks
                             and feels like a real terminal
```

---

## `[ 04 ]` // ARCHITECTURE

```
                         ┌──────────────────────┐
                         │   USER INPUT         │
                         │  (Type OR Speak)     │
                         └──────────┬───────────┘
                                    │
               ┌────────────────────▼─────────────────────┐
               │              main.py                      │
               │         Iron Man HUD Interface            │
               │  tkinter + customtkinter + canvas rings   │
               └───────┬─────────────────┬────────────────┘
                        │                 │
          ┌─────────────▼──┐     ┌────────▼────────────┐
          │   voice.py     │     │    command.py        │
          │                │     │                      │
          │  pyttsx3 (TTS) │     │  Built-in commands   │
          │  SpeechRecog   │     │  ─────────────────   │
          │  (microphone)  │     │  time / date         │
          └────────────────┘     │  open youtube        │
                                 │  search google       │
                                 │  calculator          │
                                 │  jokes               │
                                 └────────┬─────────────┘
                                          │
                                    MATCH FOUND?
                                    │         │
                                   YES        NO
                                    │         │
                              INSTANT    ┌────▼────────────┐
                              RESPONSE   │  api_client.py  │
                                         │                 │
                                         │  Anthropic SDK  │
                                         │  Chat history   │
                                         │  (last 20 msgs) │
                                         └────┬────────────┘
                                              │
                                    ┌─────────▼──────────┐
                                    │   Anthropic Cloud  │
                                    │  claude-sonnet-4   │
                                    └────────────────────┘
                                              │
                              ┌───────────────▼───────────────┐
                              │  Response → Chat bubble + TTS │
                              └───────────────────────────────┘
```

---

## `[ 05 ]` // TECH STACK

| Module | Library | Why |
|---|---|---|
| HUD Interface | `tkinter` + `customtkinter` | Native Python GUI — no browser, no Electron |
| AI Brain | `anthropic` SDK | Official Claude API with conversation history |
| Text-to-Speech | `pyttsx3` | Fully offline TTS — works without internet |
| Voice Input | `SpeechRecognition` | Google Speech API via microphone |
| Microphone Access | `pyaudio` | Low-level audio capture |
| System Stats | `psutil` | Real CPU / RAM / battery readings |
| Secrets | `python-dotenv` | API key never touches source code |

---

## `[ 06 ]` // GETTING STARTED

### Prerequisites
- Python `3.10+`
- A microphone
- Anthropic API key → [console.anthropic.com](https://console.anthropic.com/settings/keys)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/jarvis-ai.git
cd jarvis-ai

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Open .env and add: ANTHROPIC_API_KEY=sk-ant-...

# 5. Launch
python main.py
```

> **Windows — pyaudio install fail?**
> ```bash
> pip install pipwin && pipwin install pyaudio
> ```

---

## `[ 07 ]` // COMMANDS

### ⚡ Instant (no API call)

| Command | Action |
|---|---|
| `hello` / `hi` / `hey` | Time-aware greeting |
| `what time is it` | Current time |
| `what's today's date` | Full date |
| `search [anything]` | Google search in browser |
| `youtube search [query]` | YouTube search |
| `open youtube` / `open github` | Opens in browser |
| `calculate 99 * 12` | Quick math |
| `tell me a joke` | Programmer joke |
| `bye` / `exit` | Closes Jarvis |

### 🧠 Claude AI (everything else)

Anything not matched above → sent to Claude with full context:

```
You:    "Explain how neural networks work"
You:    "Write a Python function to sort a dict by value"
You:    "What did we talk about earlier?"    ← it remembers!
You:    "Translate this to Hindi: ..."
```

---

## `[ 08 ]` // CUSTOMISE

**Change Jarvis personality** → `api_client.py`:
```python
SYSTEM_PROMPT = """You are JARVIS... (rewrite this however you want)"""
```

**Add a new command** → `command.py`:
```python
if "open spotify" in q:
    webbrowser.open("https://open.spotify.com")
    return "Opening Spotify, sir."
```

**Change voice speed** → `voice.py`:
```python
_engine.setProperty("rate", 175)  # higher = faster
```

**Change ring color scheme** → `main.py` palette section:
```python
CYAN  = "#00d4ff"   # change to any hex
ORANGE = "#ff6b1a"  # thinking color
GREEN  = "#00ff88"  # listening color
```

---

## `[ 09 ]` // PROJECT STRUCTURE

```
jarvis-ai/
│
├── main.py            // Iron Man HUD — UI, animations, layout
├── command.py         // Built-in command handler
├── voice.py           // TTS (pyttsx3) + STT (SpeechRecognition)
├── api_client.py      // Claude API + conversation history
│
├── .env               // 🔑 secret API key 
├── .env.example       // Template 
├── .gitignore        
├── requirements.txt   // All dependencies
└── README.md          // This file
```

---

## `[ 10 ]` // FUTURE UPGRADES

```
  ○  Weather widget in sidebar (OpenWeatherMap API)
  ○  Spotify playback controls
  ○  Chat history saved to JSON file
  ○  Wake word detection ("Hey Jarvis...")
  ○  Multiple AI personas / personality switching
  ○  Custom hotkey to activate voice input
```

---

## `[ 11 ]` // LICENSE

```
MIT License — build on it, break it, ship it.
If it helped you, leave a ⭐
```

---

<div align="center">

```
◈ ─────────────────────────────────────────────────────────── ◈
       BUILT WITH PYTHON  ·  POWERED BY ANTHROPIC CLAUDE
            INSPIRED BY TONY STARK'S J.A.R.V.I.S
◈ ─────────────────────────────────────────────────────────── ◈
```

![Visits](https://visitor-badge.laobi.icu/badge?page_id=YOUR_USERNAME.jarvis-ai&style=flat-square&color=00d4ff&labelColor=050a0f)

</div>
