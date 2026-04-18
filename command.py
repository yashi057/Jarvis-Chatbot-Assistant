"""
Commands Module — Handles built-in commands before falling back to Claude API.
Returns None if no command matched (signals caller to use Claude).
"""

import datetime
import webbrowser
import subprocess
import platform
import sys


# ── Command Registry ──────────────────────────────────────────────────────────

def process_command(query: str) -> str | None:
    """
    Check query against built-in commands.
    Returns a response string, or None if no command matched.
    """
    q = query.lower().strip()

    # Greetings
    if any(w in q for w in ("hello", "hi ", "hey", "what's up")):
        return _greeting()

    # Time / Date
    if "time" in q:
        return "The current time is " + datetime.datetime.now().strftime("%I:%M %p")
    if "date" in q or "today" in q:
        return "Today is " + datetime.datetime.now().strftime("%A, %d %B %Y")

    # System info
    if "my system" in q or "os version" in q or "operating system" in q:
        return f"You're running {platform.system()} {platform.release()}."

    # Web — open sites
    if "open youtube" in q or "youtube" in q:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube for you."
    if "open google" in q or "open browser" in q:
        webbrowser.open("https://google.com")
        return "Opening Google."
    if "open github" in q:
        webbrowser.open("https://github.com")
        return "Opening GitHub."

    # Web — search
    if q.startswith("search ") or q.startswith("google "):
        term = q.replace("search ", "").replace("google ", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={term}")
        return f'Searching Google for "{term}".'
    if q.startswith("youtube search ") or q.startswith("search youtube "):
        term = q.replace("youtube search ", "").replace("search youtube ", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={term}")
        return f'Searching YouTube for "{term}".'

    # Calculator
    if "calculate" in q or q.startswith("what is ") and any(c in q for c in "+-*/"):
        expr = q.replace("calculate", "").replace("what is", "").strip()
        return _safe_eval(expr)

    # Jokes
    if "joke" in q or "make me laugh" in q:
        return _random_joke()

    # Exit / Goodbye
    if any(w in q for w in ("exit", "bye", "goodbye", "quit", "shut down")):
        return "Goodbye! Have a great day!"

    # No match — return None so caller falls back to Claude
    return None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _greeting() -> str:
    hour = datetime.datetime.now().hour
    if hour < 12:
        period = "morning"
    elif hour < 17:
        period = "afternoon"
    else:
        period = "evening"
    return f"Good {period}! I'm Jarvis. Ask me anything or give me a command."


def _safe_eval(expr: str) -> str | None:
    try:
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expr):
            return None  # Let Claude handle complex math questions
        result = eval(expr, {"__builtins__": {}})
        return f"The answer is {result}."
    except Exception:
        return None


def _random_joke() -> str:
    import random
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
        "Why did the Python developer go broke? Because they used all their cache.",
        "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?'",
        "Why do Java developers wear glasses? Because they don't C#.",
    ]
    return random.choice(jokes)