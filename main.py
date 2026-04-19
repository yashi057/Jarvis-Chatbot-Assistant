"""
JARVIS AI Assistant — Iron Man HUD Edition
Animated HUD, live system stats, boot sequence, typing indicator.
"""

import customtkinter as ctk
import tkinter as tk
import threading
import datetime
import math
import psutil
import webbrowser
from voice import speak, take_command
from command import process_command
from api_client import ask_claude

# ── Palette ───────────────────────────────────────────────────────────────────
BG          = "#050a0f"
BG_PANEL    = "#080e15"
BG_CARD     = "#0a1520"
BG_MSG      = "#0d1e2e"
CYAN        = "#00d4ff"
CYAN_DIM    = "#0a4a5e"
CYAN_GLOW   = "#00aacc"
ORANGE      = "#ff6b1a"
ORANGE_DIM  = "#3d1a06"
GREEN       = "#00ff88"
GREEN_DIM   = "#003320"
WHITE       = "#e8f4f8"
DIM         = "#2a4a5e"
DIMMER      = "#0f2030"
FONT_HUD    = ("Courier New", 11, "bold")
FONT_TITLE  = ("Courier New", 22, "bold")
FONT_MSG    = ("Courier New", 12)
FONT_SMALL  = ("Courier New", 10)
FONT_TINY   = ("Courier New", 9)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ── Main App ──────────────────────────────────────────────────────────────────
class JarvisHUD(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("J.A.R.V.I.S  //  MARK VII")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(fg_color=BG)

        self._listening   = False
        self._thinking    = False
        self._angle       = 0
        self._pulse       = 0
        self._scan_y      = 0
        self._boot_done   = False
        self._typing_dots = 0

        self._build_ui()
        self._start_animations()
        self._boot_sequence()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Left panel (HUD sidebar) ──
        self.left = tk.Frame(self, bg=BG_PANEL, width=280)
        self.left.pack(side="left", fill="y")
        self.left.pack_propagate(False)
        self._build_sidebar()

        # ── Divider ──
        tk.Frame(self, bg=CYAN_DIM, width=1).pack(side="left", fill="y")

        # ── Right panel (chat) ──
        self.right = tk.Frame(self, bg=BG)
        self.right.pack(side="right", fill="both", expand=True)
        self._build_chat_area()
        self._build_input_bar()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        # HUD ring canvas
        self.ring_canvas = tk.Canvas(
            self.left, width=240, height=240,
            bg=BG_PANEL, highlightthickness=0
        )
        self.ring_canvas.pack(pady=(24, 0))

        # Status text under ring
        self.status_var = tk.StringVar(value="[ SYSTEM ONLINE ]")
        tk.Label(
            self.left, textvariable=self.status_var,
            font=FONT_HUD, bg=BG_PANEL, fg=CYAN
        ).pack(pady=(8, 0))

        self.mode_var = tk.StringVar(value="MODE: STANDBY")
        tk.Label(
            self.left, textvariable=self.mode_var,
            font=FONT_TINY, bg=BG_PANEL, fg=DIM
        ).pack(pady=(2, 16))

        # Divider
        tk.Frame(self.left, bg=CYAN_DIM, height=1).pack(fill="x", padx=20)

        # System stats
        tk.Label(
            self.left, text="[ SYSTEM DIAGNOSTICS ]",
            font=FONT_TINY, bg=BG_PANEL, fg=DIM
        ).pack(pady=(14, 6))

        self.cpu_bar  = self._stat_row("CPU LOAD")
        self.ram_bar  = self._stat_row("MEMORY")
        self.bat_bar  = self._stat_row("POWER CELL")

        tk.Frame(self.left, bg=CYAN_DIM, height=1).pack(fill="x", padx=20, pady=14)

        # Clock
        self.clock_var = tk.StringVar()
        tk.Label(
            self.left, textvariable=self.clock_var,
            font=("Courier New", 28, "bold"), bg=BG_PANEL, fg=WHITE
        ).pack()
        self.date_var = tk.StringVar()
        tk.Label(
            self.left, textvariable=self.date_var,
            font=FONT_TINY, bg=BG_PANEL, fg=DIM
        ).pack(pady=(2, 16))

        tk.Frame(self.left, bg=CYAN_DIM, height=1).pack(fill="x", padx=20)

        # Quick actions
        tk.Label(
            self.left, text="[ QUICK ACCESS ]",
            font=FONT_TINY, bg=BG_PANEL, fg=DIM
        ).pack(pady=(14, 8))

        self._hud_btn("▶  YOUTUBE",  lambda: webbrowser.open("https://youtube.com"))
        self._hud_btn("◉  GOOGLE",   lambda: webbrowser.open("https://google.com"))
        self._hud_btn("⌂  GITHUB",   lambda: webbrowser.open("https://github.com"))
        self._hud_btn("✕  CLEAR LOG", self._clear_chat)

    def _stat_row(self, label: str):
        row = tk.Frame(self.left, bg=BG_PANEL)
        row.pack(fill="x", padx=20, pady=3)
        tk.Label(row, text=label, font=FONT_TINY, bg=BG_PANEL,
                 fg=DIM, width=12, anchor="w").pack(side="left")
        canvas = tk.Canvas(row, width=100, height=10,
                           bg=DIMMER, highlightthickness=0)
        canvas.pack(side="left", padx=(6, 4))
        val_lbl = tk.Label(row, text="0%", font=FONT_TINY,
                           bg=BG_PANEL, fg=CYAN, width=5)
        val_lbl.pack(side="left")
        return canvas, val_lbl

    def _hud_btn(self, text, cmd):
        btn = tk.Button(
            self.left, text=text, command=cmd,
            font=FONT_SMALL, bg=DIMMER, fg=CYAN,
            activebackground=CYAN_DIM, activeforeground=WHITE,
            relief="flat", cursor="hand2", bd=0,
            padx=10, pady=6
        )
        btn.pack(fill="x", padx=20, pady=3)
        btn.bind("<Enter>", lambda e: btn.config(bg=CYAN_DIM))
        btn.bind("<Leave>", lambda e: btn.config(bg=DIMMER))

    # ── Chat Area ─────────────────────────────────────────────────────────────
    def _build_chat_area(self):
        # Top bar
        topbar = tk.Frame(self.right, bg=BG_PANEL, height=48)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(
            topbar, text="  ◈  JARVIS  //  CONVERSATIONAL INTERFACE",
            font=FONT_HUD, bg=BG_PANEL, fg=CYAN, anchor="w"
        ).pack(side="left", fill="y")

        self.conn_label = tk.Label(
            topbar, text="◉ CLAUDE API  ", font=FONT_TINY,
            bg=BG_PANEL, fg=GREEN
        )
        self.conn_label.pack(side="right", fill="y")

        # Scan line canvas overlay + chat frame together
        self.chat_outer = tk.Frame(self.right, bg=BG)
        self.chat_outer.pack(fill="both", expand=True)

        self.chat_scroll = ctk.CTkScrollableFrame(
            self.chat_outer, fg_color=BG, corner_radius=0
        )
        self.chat_scroll.pack(fill="both", expand=True, padx=0, pady=0)

        # Typing indicator
        self.typing_frame = tk.Frame(self.chat_scroll, bg=BG)
        self.typing_label = tk.Label(
            self.typing_frame, text="",
            font=FONT_MSG, bg=BG, fg=CYAN_GLOW
        )
        self.typing_label.pack(anchor="w", padx=20)

    def _build_input_bar(self):
        bar = tk.Frame(self.right, bg=BG_PANEL, height=72)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # Border top
        tk.Frame(bar, bg=CYAN_DIM, height=1).pack(fill="x")

        inner = tk.Frame(bar, bg=BG_PANEL)
        inner.pack(fill="both", expand=True, padx=16, pady=10)

        # Prompt label
        tk.Label(
            inner, text="▶ INPUT:", font=FONT_HUD,
            bg=BG_PANEL, fg=ORANGE
        ).pack(side="left", padx=(0, 8))

        self.entry = tk.Entry(
            inner, font=FONT_MSG, bg=BG_CARD, fg=WHITE,
            insertbackground=CYAN, relief="flat",
            bd=0, highlightthickness=1,
            highlightbackground=DIM, highlightcolor=CYAN
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.entry.bind("<Return>", lambda _: self._send_text())

        self.voice_btn = tk.Button(
            inner, text="🎤", font=("Segoe UI Emoji", 16),
            bg=DIMMER, fg=CYAN, activebackground=ORANGE_DIM,
            relief="flat", cursor="hand2", padx=10,
            command=self._voice_input
        )
        self.voice_btn.pack(side="right", padx=(8, 0))
        self.voice_btn.bind("<Enter>", lambda e: self.voice_btn.config(bg=CYAN_DIM))
        self.voice_btn.bind("<Leave>", lambda e: self.voice_btn.config(bg=DIMMER))

        self.send_btn = tk.Button(
            inner, text="TRANSMIT ▶▶",
            font=FONT_HUD, bg=CYAN, fg=BG,
            activebackground=CYAN_GLOW, activeforeground=BG,
            relief="flat", cursor="hand2", padx=14,
            command=self._send_text
        )
        self.send_btn.pack(side="right", padx=(8, 0))

    # ── Messages ──────────────────────────────────────────────────────────────
    def _add_msg(self, sender: str, text: str, is_boot=False):
        now   = datetime.datetime.now().strftime("%H:%M:%S")
        is_me = sender in ("YOU", "YOU (VOICE)")
        color = ORANGE if is_me else CYAN
        bg    = "#0f1e2a" if not is_me else "#1a0f0a"
        prefix = f"[{now}] {sender} ▶▶"

        outer = tk.Frame(self.chat_scroll, bg=BG, pady=3)
        outer.pack(fill="x", padx=12)

        tk.Label(
            outer, text=prefix, font=FONT_TINY,
            bg=BG, fg=color, anchor="w"
        ).pack(fill="x")

        bubble = tk.Frame(outer, bg=bg, padx=14, pady=8)
        bubble.pack(fill="x", pady=(2, 0))

        # Left color bar
        tk.Frame(bubble, bg=color, width=2).pack(side="left", fill="y", padx=(0, 10))

        tk.Label(
            bubble, text=text, font=FONT_MSG,
            bg=bg, fg=WHITE, anchor="w",
            justify="left", wraplength=640
        ).pack(side="left", fill="x", expand=True)

        # Scroll to bottom
        self.after(60, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))

    def _add_system_line(self, text: str, color=DIM):
        tk.Label(
            self.chat_scroll, text=f"  //  {text}",
            font=FONT_TINY, bg=BG, fg=color, anchor="w"
        ).pack(fill="x", padx=20, pady=1)
        self.after(60, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))

    def _clear_chat(self):
        for w in self.chat_scroll.winfo_children():
            w.destroy()
        self._add_system_line("LOG CLEARED", DIM)

    # ── Boot Sequence ─────────────────────────────────────────────────────────
    def _boot_sequence(self):
        lines = [
            ("INITIALIZING J.A.R.V.I.S  MARK VII ...", CYAN, 0),
            ("LOADING NEURAL PATHWAYS ...", DIM, 300),
            ("VOICE ENGINE: ONLINE", GREEN, 600),
            ("SPEECH RECOGNITION: ONLINE", GREEN, 900),
            ("CLAUDE API: CONNECTING ...", ORANGE, 1200),
            ("ALL SYSTEMS NOMINAL. WELCOME BACK.", CYAN, 1800),
        ]
        for text, color, delay in lines:
            self.after(delay, lambda t=text, c=color: self._add_system_line(t, c))

        self.after(2200, self._boot_greet)

    def _boot_greet(self):
        self._boot_done = True
        hour = datetime.datetime.now().hour
        greet = "Good morning" if hour < 12 else "Good evening" if hour >= 17 else "Good afternoon"
        msg = f"{greet}. All systems online. How can I assist you today?"
        self._add_msg("JARVIS", msg)
        threading.Thread(target=lambda: speak(msg), daemon=True).start()

    # ── Actions ───────────────────────────────────────────────────────────────
    def _send_text(self):
        query = self.entry.get().strip()
        if not query:
            return
        self.entry.delete(0, "end")
        self._add_msg("YOU", query)
        threading.Thread(target=self._handle, args=(query,), daemon=True).start()

    def _voice_input(self):
        if self._listening:
            return
        threading.Thread(target=self._do_voice, daemon=True).start()

    def _do_voice(self):
        self._listening = True
        self.after(0, lambda: [
            self.voice_btn.config(bg=ORANGE, fg=BG),
            self.status_var.set("[ LISTENING... ]"),
            self.mode_var.set("MODE: VOICE INPUT")
        ])
        query = take_command()
        self._listening = False
        self.after(0, lambda: self.voice_btn.config(bg=DIMMER, fg=CYAN))
        if query:
            self.after(0, lambda: self._add_msg("YOU (VOICE)", query))
            self._handle(query)
        else:
            self.after(0, lambda: self._set_status("STANDBY"))

    def _handle(self, query: str):
        self._thinking = True
        self.after(0, lambda: self._set_status("PROCESSING"))
        self.after(0, self._show_typing)

        response = process_command(query)
        if response is None:
            response = ask_claude(query)

        self._thinking = False
        self.after(0, self._hide_typing)
        self.after(0, lambda: self._add_msg("JARVIS", response))
        self.after(0, lambda: self._set_status("STANDBY"))
        speak(response)

        if any(w in query.lower() for w in ("exit", "bye", "goodbye")):
            self.after(2000, self.quit)

    def _show_typing(self):
        self.typing_frame.pack(fill="x", before=self.chat_scroll.winfo_children()[-1]
                               if self.chat_scroll.winfo_children() else None)
        self._animate_typing()

    def _hide_typing(self):
        self.typing_frame.pack_forget()

    def _animate_typing(self):
        if not self._thinking:
            return
        dots = "." * (self._typing_dots % 4)
        self.typing_label.config(text=f"  JARVIS IS PROCESSING {dots}")
        self._typing_dots += 1
        self.after(400, self._animate_typing)

    def _set_status(self, mode: str):
        modes = {
            "STANDBY":    ("[ SYSTEM ONLINE ]",    "MODE: STANDBY",      CYAN),
            "PROCESSING": ("[ PROCESSING ... ]",   "MODE: NEURAL ACTIVE", ORANGE),
            "VOICE":      ("[ LISTENING ... ]",    "MODE: VOICE INPUT",   GREEN),
        }
        label, sub, color = modes.get(mode, modes["STANDBY"])
        self.status_var.set(label)
        self.mode_var.set(sub)

    # ── Animations ────────────────────────────────────────────────────────────
    def _start_animations(self):
        self._animate_ring()
        self._animate_stats()
        self._update_clock()

    def _animate_ring(self):
        c = self.ring_canvas
        c.delete("all")
        cx, cy, r = 120, 120, 90

        # Outer static rings
        for radius, col, w in [(r+22, CYAN_DIM, 1), (r+14, CYAN_DIM, 1), (r+6, DIM, 1)]:
            c.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                         outline=col, width=w)

        # Rotating arc
        start = -self._angle
        color = ORANGE if self._thinking else CYAN if self._listening else CYAN_GLOW
        extent = 300 if self._thinking else 240
        c.create_arc(cx-r, cy-r, cx+r, cy+r,
                    start=start, extent=extent,
                    outline=color, width=3, style="arc")

        # Counter arc
        c.create_arc(cx-r+8, cy-r+8, cx+r-8, cy+r-8,
                    start=start+180, extent=60,
                    outline=DIM, width=1, style="arc")

        # Inner pulsing circle
        pulse_r = 28 + int(6 * math.sin(self._pulse * 0.15))
        p_color = ORANGE if self._thinking else GREEN if self._listening else CYAN
        c.create_oval(cx-pulse_r, cy-pulse_r, cx+pulse_r, cy+pulse_r,
                     outline=p_color, width=2)

        # Center dot
        c.create_oval(cx-4, cy-4, cx+4, cy+4, fill=p_color, outline="")

        # Tick marks
        for i in range(12):
            angle_r = math.radians(i * 30)
            x1 = cx + (r+6)  * math.cos(angle_r)
            y1 = cy + (r+6)  * math.sin(angle_r)
            x2 = cx + (r+12) * math.cos(angle_r)
            y2 = cy + (r+12) * math.sin(angle_r)
            c.create_line(x1, y1, x2, y2,
                         fill=CYAN if i % 3 == 0 else DIM, width=1)

        self._angle = (self._angle + (4 if self._thinking else 2)) % 360
        self._pulse += 1
        self.after(40, self._animate_ring)

    def _animate_stats(self):
        try:
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent
            bat = psutil.sensors_battery()
            bat_pct = bat.percent if bat else 100

            self._draw_bar(self.cpu_bar, cpu)
            self._draw_bar(self.ram_bar, ram)
            self._draw_bar(self.bat_bar, bat_pct, invert=True)
        except Exception:
            pass
        self.after(1500, self._animate_stats)

    def _draw_bar(self, bar_tuple, value: float, invert=False):
        canvas, label = bar_tuple
        canvas.delete("all")
        w, h = 100, 10
        fill = int((value / 100) * w)
        color = GREEN if value < 60 else ORANGE if value < 85 else "#ff3333"
        if invert:
            color = GREEN if value > 40 else ORANGE if value > 20 else "#ff3333"
        canvas.create_rectangle(0, 0, w, h, fill=DIMMER, outline=DIM)
        canvas.create_rectangle(0, 0, fill, h, fill=color, outline="")
        label.config(text=f"{int(value)}%", fg=color)

    def _update_clock(self):
        now = datetime.datetime.now()
        self.clock_var.set(now.strftime("%H:%M:%S"))
        self.date_var.set(now.strftime("%A  //  %d %b %Y").upper())
        self.after(1000, self._update_clock)


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = JarvisHUD()
    app.mainloop()
