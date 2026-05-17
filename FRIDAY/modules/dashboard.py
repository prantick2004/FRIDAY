import tkinter as tk
import threading
import datetime
import psutil
import os
import sys

sys.path.append(os.path.expanduser("~") + "/FRIDAY/modules")

class FridayDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FRIDAY AI")
        self.root.geometry("400x600")
        self.root.configure(bg="#0a0a1a")
        self.root.attributes('-topmost', False)
        self.root.resizable(False, False)

        # ── HEADER ────────────────────────────────────
        header = tk.Frame(self.root, bg="#0a0a1a")
        header.pack(fill='x', pady=10)

        tk.Label(
            header,
            text="⬡ FRIDAY AI ⬡",
            font=("Courier", 22, "bold"),
            fg="#00ffcc",
            bg="#0a0a1a"
        ).pack()

        tk.Label(
            header,
            text="IRON MAN AI SYSTEM",
            font=("Courier", 10),
            fg="#005544",
            bg="#0a0a1a"
        ).pack()

        # ── SEPARATOR ─────────────────────────────────
        tk.Frame(
            self.root,
            bg="#00ffcc",
            height=1
        ).pack(fill='x', padx=20)

        # ── STATUS ────────────────────────────────────
        status_frame = tk.Frame(self.root, bg="#0a0a1a")
        status_frame.pack(fill='x', padx=20, pady=10)

        self.status_label = tk.Label(
            status_frame,
            text="● ONLINE",
            font=("Courier", 12, "bold"),
            fg="#00ff00",
            bg="#0a0a1a"
        )
        self.status_label.pack()

        self.time_label = tk.Label(
            status_frame,
            text="",
            font=("Courier", 28, "bold"),
            fg="#00ffcc",
            bg="#0a0a1a"
        )
        self.time_label.pack(pady=5)

        self.date_label = tk.Label(
            status_frame,
            text="",
            font=("Courier", 11),
            fg="#008866",
            bg="#0a0a1a"
        )
        self.date_label.pack()

        # ── SEPARATOR ─────────────────────────────────
        tk.Frame(
            self.root,
            bg="#003333",
            height=1
        ).pack(fill='x', padx=20, pady=10)

        # ── SYSTEM STATS ──────────────────────────────
        stats_frame = tk.Frame(self.root, bg="#0a0a1a")
        stats_frame.pack(fill='x', padx=20)

        tk.Label(
            stats_frame,
            text="SYSTEM STATUS",
            font=("Courier", 10, "bold"),
            fg="#006655",
            bg="#0a0a1a"
        ).pack()

        self.cpu_label = tk.Label(
            stats_frame,
            text="CPU: ---%",
            font=("Courier", 12),
            fg="#00ffcc",
            bg="#0a0a1a"
        )
        self.cpu_label.pack(pady=2)

        self.ram_label = tk.Label(
            stats_frame,
            text="RAM: ---%",
            font=("Courier", 12),
            fg="#00ffcc",
            bg="#0a0a1a"
        )
        self.ram_label.pack(pady=2)

        self.battery_label = tk.Label(
            stats_frame,
            text="BAT: ---%",
            font=("Courier", 12),
            fg="#00ffcc",
            bg="#0a0a1a"
        )
        self.battery_label.pack(pady=2)

        # ── SEPARATOR ─────────────────────────────────
        tk.Frame(
            self.root,
            bg="#003333",
            height=1
        ).pack(fill='x', padx=20, pady=10)

        # ── FRIDAY RESPONSE ───────────────────────────
        tk.Label(
            self.root,
            text="FRIDAY SAYS",
            font=("Courier", 10, "bold"),
            fg="#006655",
            bg="#0a0a1a"
        ).pack()

        self.response_label = tk.Label(
            self.root,
            text="Initializing systems...",
            font=("Courier", 11),
            fg="#ffffff",
            bg="#0a0a1a",
            wraplength=360,
            justify='center'
        )
        self.response_label.pack(pady=10, padx=20)

        # ── LISTENING STATUS ──────────────────────────
        self.listen_label = tk.Label(
            self.root,
            text="◉ LISTENING",
            font=("Courier", 12, "bold"),
            fg="#00ff00",
            bg="#0a0a1a"
        )
        self.listen_label.pack(pady=5)

        # ── SEPARATOR ─────────────────────────────────
        tk.Frame(
            self.root,
            bg="#003333",
            height=1
        ).pack(fill='x', padx=20, pady=10)

        # ── QUICK COMMANDS ────────────────────────────
        tk.Label(
            self.root,
            text="QUICK COMMANDS",
            font=("Courier", 10, "bold"),
            fg="#006655",
            bg="#0a0a1a"
        ).pack()

        btn_frame = tk.Frame(self.root, bg="#0a0a1a")
        btn_frame.pack(pady=10)

        buttons = [
            ("WEATHER", "weather"),
            ("NEWS", "news"),
            ("STATUS", "system status"),
            ("GMAIL", "open gmail"),
        ]

        for i, (label, cmd) in enumerate(buttons):
            btn = tk.Button(
                btn_frame,
                text=label,
                font=("Courier", 9, "bold"),
                fg="#00ffcc",
                bg="#001122",
                activebackground="#003344",
                activeforeground="#00ffcc",
                relief='flat',
                width=8,
                command=lambda c=cmd: self.quick_command(c)
            )
            btn.grid(row=0, column=i, padx=5)

        # ── FOOTER ────────────────────────────────────
        tk.Frame(
            self.root,
            bg="#00ffcc",
            height=1
        ).pack(fill='x', padx=20, pady=10)

        tk.Label(
            self.root,
            text="FRIDAY v1.0 — Built by Prantick",
            font=("Courier", 8),
            fg="#003333",
            bg="#0a0a1a"
        ).pack()

        # Start update loop
        self.process_func = None
        self.update_stats()

    def set_process_func(self, func):
        self.process_func = func

    def quick_command(self, cmd):
        if self.process_func:
            threading.Thread(
                target=self.process_func,
                args=(cmd,),
                daemon=True
            ).start()

    def update_response(self, text):
        self.response_label.config(text=text)

    def set_listening(self, listening):
        if listening:
            self.listen_label.config(
                text="◉ LISTENING",
                fg="#00ff00"
            )
            self.status_label.config(
                text="● ONLINE",
                fg="#00ff00"
            )
        else:
            self.listen_label.config(
                text="◎ PROCESSING",
                fg="#ffaa00"
            )

    def update_stats(self):
        now = datetime.datetime.now()
        self.time_label.config(
            text=now.strftime("%I:%M:%S %p")
        )
        self.date_label.config(
            text=now.strftime("%A, %B %d %Y")
        )

        cpu = psutil.cpu_percent()
        self.cpu_label.config(text=f"CPU: {int(cpu)}%")

        ram = psutil.virtual_memory().percent
        self.ram_label.config(text=f"RAM: {int(ram)}%")

        b = psutil.sensors_battery()
        if b:
            bat_color = "#00ff00" if b.percent > 20 else "#ff4444"
            plug = "⚡" if b.power_plugged else "🔋"
            self.battery_label.config(
                text=f"BAT: {int(b.percent)}% {plug}",
                fg=bat_color
            )

        self.root.after(1000, self.update_stats)

    def run(self):
        self.root.mainloop()