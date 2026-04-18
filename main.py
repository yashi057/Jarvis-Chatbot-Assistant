"""
JARVIS AI Assistant
A modern AI-powered desktop assistant with voice input and Claude API integration.
"""

import customtkinter as ctk
import threading
import datetime
import webbrowser
from voice import speak, take_command
from command import process_command
from api_client import ask_claude

# ── Theme Setup ──────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT    = "#00BFFF"
BG_DARK   = "#0d0d0d"
BG_PANEL  = "#111827"
BG_CARD   = "#1f2937"
TEXT_DIM  = "#6b7280"
TEXT_MAIN = "#e5e7eb"
USER_CLR  = "#3b82f6"
BOT_CLR   = "#00BFFF"
FONT_MAIN = ("Segoe UI", 14)
FONT_BOLD = ("Segoe UI", 14, "bold")
FONT_SMALL= ("Segoe UI", 11)


# ── Main Window ───────────────────────────────────────────────────────────────
class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JARVIS — AI Assistant")
        self.geometry("900x680")
        self.minsize(700, 500)
        self.configure(fg_color=BG_DARK)

        self._is_listening = False
        self._build_layout()
        self._welcome()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        # Left sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=BG_PANEL, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        # Main chat area
        self.main_frame = ctk.CTkFrame(self, fg_color=BG_DARK)
        self.main_frame.pack(side="right", fill="both", expand=True)
        self._build_chat()
        self._build_input_bar()

    def _build_sidebar(self):
        # Logo / Title
        ctk.CTkLabel(
            self.sidebar, text="J.A.R.V.I.S",
            font=("Segoe UI", 22, "bold"), text_color=ACCENT
        ).pack(pady=(28, 2))
        ctk.CTkLabel(
            self.sidebar, text="AI Desktop Assistant",
            font=FONT_SMALL, text_color=TEXT_DIM
        ).pack(pady=(0, 24))

        ctk.CTkFrame(self.sidebar, height=1, fg_color="#374151").pack(fill="x", padx=20)

        # Clock label
        self.clock_label = ctk.CTkLabel(
            self.sidebar, text="", font=("Consolas", 20, "bold"),
            text_color=TEXT_MAIN
        )
        self.clock_label.pack(pady=(20, 0))
        self.date_label = ctk.CTkLabel(
            self.sidebar, text="", font=FONT_SMALL, text_color=TEXT_DIM
        )
        self.date_label.pack(pady=(2, 20))
        self._update_clock()

        ctk.CTkFrame(self.sidebar, height=1, fg_color="#374151").pack(fill="x", padx=20)

        # Quick-action buttons
        ctk.CTkLabel(
            self.sidebar, text="QUICK ACTIONS",
            font=("Segoe UI", 10, "bold"), text_color=TEXT_DIM
        ).pack(pady=(18, 8))

        self._sidebar_btn("🌐  Google",   lambda: webbrowser.open("https://google.com"))
        self._sidebar_btn("▶  YouTube",  lambda: webbrowser.open("https://youtube.com"))
        self._sidebar_btn("🗑  Clear Chat", self._clear_chat)

        # Status indicator
        self.status_label = ctk.CTkLabel(
            self.sidebar, text="● Ready", font=FONT_SMALL, text_color="#22c55e"
        )
        self.status_label.pack(side="bottom", pady=20)

    def _sidebar_btn(self, text, command):
        ctk.CTkButton(
            self.sidebar, text=text, command=command,
            fg_color=BG_CARD, hover_color="#374151",
            text_color=TEXT_MAIN, anchor="w",
            height=36, corner_radius=8,
            font=FONT_SMALL
        ).pack(fill="x", padx=16, pady=4)

    def _build_chat(self):
        self.chat_frame = ctk.CTkScrollableFrame(
            self.main_frame, fg_color=BG_DARK, corner_radius=0
        )
        self.chat_frame.pack(fill="both", expand=True, padx=12, pady=(12, 0))

    def _build_input_bar(self):
        bar = ctk.CTkFrame(self.main_frame, fg_color=BG_PANEL, corner_radius=12, height=72)
        bar.pack(fill="x", padx=12, pady=12)
        bar.pack_propagate(False)

        self.entry = ctk.CTkEntry(
            bar, placeholder_text="Ask Jarvis anything...",
            font=FONT_MAIN, height=44, corner_radius=10,
            fg_color=BG_CARD, border_color="#374151",
            text_color=TEXT_MAIN
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(12, 8), pady=14)
        self.entry.bind("<Return>", lambda _: self._send_text())

        self.voice_btn = ctk.CTkButton(
            bar, text="🎤", width=48, height=44,
            font=("Segoe UI", 18), corner_radius=10,
            fg_color=BG_CARD, hover_color="#374151",
            command=self._voice_input
        )
        self.voice_btn.pack(side="right", padx=(0, 8), pady=14)

        ctk.CTkButton(
            bar, text="Send", width=90, height=44,
            font=FONT_BOLD, corner_radius=10,
            fg_color=ACCENT, hover_color="#0099cc",
            text_color=BG_DARK,
            command=self._send_text
        ).pack(side="right", padx=(0, 12), pady=14)

    # ── Chat Bubbles ──────────────────────────────────────────────────────────
    def _add_bubble(self, sender: str, message: str):
        is_user = sender == "You"
        color   = USER_CLR if is_user else BOT_CLR
        side    = "e" if is_user else "w"
        label   = sender.upper()

        outer = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        outer.pack(fill="x", pady=4, padx=8)

        ctk.CTkLabel(
            outer, text=label,
            font=("Segoe UI", 10, "bold"), text_color=color,
            anchor="e" if is_user else "w"
        ).pack(anchor=side)

        bubble = ctk.CTkLabel(
            outer, text=message,
            font=FONT_MAIN, text_color=TEXT_MAIN,
            fg_color=BG_CARD if not is_user else "#1e3a5f",
            corner_radius=12, wraplength=540,
            justify="left", anchor="w",
            padx=14, pady=10
        )
        bubble.pack(anchor=side, pady=(2, 0))

        # Auto-scroll
        self.after(50, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    def _add_system_msg(self, msg: str):
        ctk.CTkLabel(
            self.chat_frame, text=msg,
            font=FONT_SMALL, text_color=TEXT_DIM
        ).pack(pady=6)

    # ── Actions ───────────────────────────────────────────────────────────────
    def _send_text(self):
        query = self.entry.get().strip()
        if not query:
            return
        self.entry.delete(0, "end")
        self._add_bubble("You", query)
        threading.Thread(target=self._handle_query, args=(query,), daemon=True).start()

    def _voice_input(self):
        if self._is_listening:
            return
        threading.Thread(target=self._do_voice, daemon=True).start()

    def _do_voice(self):
        self._is_listening = True
        self._set_status("🎙 Listening...", "#f59e0b")
        self.voice_btn.configure(fg_color="#f59e0b")
        query = take_command()
        self.voice_btn.configure(fg_color=BG_CARD)
        self._is_listening = False
        self._set_status("● Ready", "#22c55e")
        if query:
            self.after(0, lambda: self._add_bubble("You (voice)", query))
            self._handle_query(query)

    def _handle_query(self, query: str):
        self._set_status("⚙ Thinking...", ACCENT)
        response = process_command(query)

        # If built-in command didn't match, fall back to Claude API
        if response is None:
            response = ask_claude(query)

        self.after(0, lambda: self._add_bubble("Jarvis", response))
        speak(response)
        self._set_status("● Ready", "#22c55e")

        # Handle quit command
        if query.lower() in ("exit", "bye", "goodbye"):
            self.after(1500, self.quit)

    def _clear_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self._add_system_msg("— Chat cleared —")

    # ── Clock ─────────────────────────────────────────────────────────────────
    def _update_clock(self):
        now = datetime.datetime.now()
        self.clock_label.configure(text=now.strftime("%H:%M:%S"))
        self.date_label.configure(text=now.strftime("%d %b %Y"))
        self.after(1000, self._update_clock)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _set_status(self, text: str, color: str):
        self.after(0, lambda: self.status_label.configure(text=text, text_color=color))

    def _welcome(self):
        hour = datetime.datetime.now().hour
        greet = "Good morning" if hour < 12 else "Good evening" if hour >= 17 else "Good afternoon"
        msg = f"{greet}! I'm Jarvis. How can I help you today?"
        self._add_bubble("Jarvis", msg)
        threading.Thread(target=lambda: speak(msg), daemon=True).start()


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()