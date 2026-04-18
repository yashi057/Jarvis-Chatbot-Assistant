"""
Voice Module — Text-to-Speech and Speech Recognition
"""

import pyttsx3
import speech_recognition as sr

# ── TTS Engine ────────────────────────────────────────────────────────────────
_engine = pyttsx3.init()
_engine.setProperty("rate", 175)
_engine.setProperty("volume", 0.9)

# Try to pick a better voice (Windows: "David" or "Zira")
voices = _engine.getProperty("voices")
for v in voices:
    if "david" in v.name.lower() or "en" in v.id.lower():
        _engine.setProperty("voice", v.id)
        break


def speak(text: str) -> None:
    """Convert text to speech (blocking)."""
    try:
        _engine.say(text)
        _engine.runAndWait()
    except RuntimeError:
        pass  # already running — skip


# ── STT ───────────────────────────────────────────────────────────────────────
def take_command() -> str:
    """Listen for a voice command and return transcribed text (lowercase).
    Returns empty string on failure.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            recognizer.pause_threshold = 1.0
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)

        query = recognizer.recognize_google(audio, language="en-in")
        return query.lower()

    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "network error on speech recognition"
    except Exception:
        return ""