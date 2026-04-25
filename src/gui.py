"""
GUI Module - Modern Clean Design
S'gaw Karen Keyboard Interface
"""

import tkinter as tk
import os
import sys
from .mappings import KEYBOARD_LAYOUT


def get_icon_path():
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'S_gawKeyboardApp.ico')


class Theme:
    BG_PRIMARY   = '#0f1117'
    BG_CARD      = '#181c27'
    BG_ELEVATED  = '#1e2235'
    BG_KEY       = '#1e2235'
    BG_KEY_HOVER = '#272d45'

    GREEN        = '#4ade80'
    GREEN_DIM    = '#16a34a'
    ORANGE       = '#fb923c'
    BLUE         = '#60a5fa'
    RED          = '#f87171'

    TEXT         = '#f1f5f9'
    TEXT_SUB     = '#94a3b8'
    TEXT_MUTED   = '#475569'

    BORDER       = '#252b40'
    BORDER_HOVER = '#60a5fa'


# ---------------------------------------------------------------------------
# Custom widgets
# ---------------------------------------------------------------------------

class ToggleSwitch(tk.Canvas):
    """Animated iOS-style pill toggle switch."""

    W, H, PAD = 56, 28, 3

    def __init__(self, parent, command=None, **kwargs):
        super().__init__(parent, width=self.W, height=self.H,
                         bg=Theme.BG_CARD, highlightthickness=0, **kwargs)
        self.command = command
        self._active = False
        self._animating = False
        self._knob_x = self._off_x()
        self._draw()
        self.bind('<Button-1>', self._on_click)
        self.bind('<Enter>', lambda e: self.configure(cursor='hand2'))

    def _off_x(self):
        return self.PAD + (self.H - 2 * self.PAD) / 2

    def _on_x(self):
        return self.W - self.PAD - (self.H - 2 * self.PAD) / 2

    def _draw(self):
        self.delete('all')
        w, h = self.W, self.H
        r = h / 2
        color = Theme.GREEN_DIM if self._active else '#334155'

        # Pill track
        self.create_arc(0, 0, h, h, start=90, extent=180,
                        fill=color, outline='')
        self.create_arc(w - h, 0, w, h, start=-90, extent=180,
                        fill=color, outline='')
        self.create_rectangle(r, 0, w - r, h, fill=color, outline='')

        # Knob
        kr = r - self.PAD
        kx = self._knob_x
        self.create_oval(kx - kr, self.PAD, kx + kr, h - self.PAD,
                         fill='white', outline='')

    def _on_click(self, _event):
        if not self._animating:
            self._active = not self._active
            self._animate(self._on_x() if self._active else self._off_x())
            if self.command:
                self.command()

    def _animate(self, target):
        self._animating = True
        diff = target - self._knob_x
        if abs(diff) < 0.8:
            self._knob_x = target
            self._animating = False
            self._draw()
            return
        self._knob_x += diff * 0.28
        self._draw()
        self.after(14, lambda: self._animate(target))

    def set_active(self, active):
        """Sync state without triggering command."""
        self._active = active
        self._knob_x = self._on_x() if active else self._off_x()
        self._draw()


class KeyButton(tk.Canvas):
    """Flat keyboard key with hover highlight border."""

    def __init__(self, parent, label, karen_char, shift_char, size=1.0):
        w = int(70 * size)
        h = int(80 * size)
        super().__init__(parent, width=w, height=h,
                         bg=Theme.BG_KEY, highlightthickness=1,
                         highlightbackground=Theme.BORDER)
        self.label = label
        self.karen_char = karen_char
        self.shift_char = shift_char
        self.size = size
        self.w, self.h = w, h
        self._draw(False)
        self.bind('<Enter>', lambda e: self._draw(True))
        self.bind('<Leave>', lambda e: self._draw(False))

    def _draw(self, hover):
        self.delete('all')
        self.configure(
            bg=Theme.BG_KEY_HOVER if hover else Theme.BG_KEY,
            highlightbackground=Theme.BORDER_HOVER if hover else Theme.BORDER,
        )
        w, h = self.w, self.h

        # Shift character (top-right, orange)
        if self.shift_char and self.shift_char.strip():
            fs = max(8, int(9 * self.size))
            self.create_text(w - 5, 5, text=self.shift_char,
                             font=('Myanmar Text', fs),
                             fill=Theme.ORANGE, anchor='ne')

        # Main character (center, green)
        if self.karen_char and self.karen_char.strip():
            fs = max(14, int(17 * self.size))
            self.create_text(w // 2, h // 2 + 8, text=self.karen_char,
                             font=('Myanmar Text', fs, 'bold'),
                             fill=Theme.GREEN, anchor='center')

        # Key label (bottom-left, muted)
        fs = max(7, int(7 * self.size))
        self.create_text(5, h - 4, text=self.label.upper(),
                         font=('Segoe UI', fs),
                         fill=Theme.TEXT_MUTED, anchor='sw')


class Divider(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=Theme.BORDER, height=1, **kwargs)


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow:
    def __init__(self, keyboard_hook, settings, tray_icon):
        self.keyboard_hook = keyboard_hook
        self.settings = settings
        self.tray_icon = tray_icon
        self.root = None
        self.toggle_switch = None
        self.toggle_label = None
        self.status_dot = None
        self.status_label = None
        self.size_multiplier = 1.0

    def _set_window_icon(self):
        try:
            path = get_icon_path()
            if os.path.exists(path):
                self.root.iconbitmap(path)
        except Exception as e:
            print(f"Warning: Could not set window icon: {e}")

    def create_window(self):
        self.root = tk.Tk()
        self.root.title("S'gaw Karen Keyboard")
        self.root.configure(bg=Theme.BG_PRIMARY)
        self._set_window_icon()

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        if sh <= 768:
            ww, wh = min(1040, sw - 50), min(650, sh - 80)
            self.size_multiplier = 0.85
        elif sh <= 900:
            ww, wh = min(1090, sw - 50), min(720, sh - 80)
            self.size_multiplier = 0.95
        elif sh <= 1080:
            ww, wh = 1140, 770
            self.size_multiplier = 1.0
        else:
            ww, wh = 1240, 850
            self.size_multiplier = 1.1

        x = (sw - ww) // 2
        y = max(20, (sh - wh) // 6)
        self.root.geometry(f"{ww}x{wh}+{x}+{y}")
        self.root.minsize(800, 530)

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.root.bind('<Escape>', lambda e: self.minimize_to_tray())

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        outer = tk.Frame(self.root, bg=Theme.BG_PRIMARY)
        outer.pack(fill='both', expand=True, padx=28, pady=22)
        self._create_header(outer)
        self._create_status_card(outer)
        self._create_keyboard_section(outer)
        self._create_footer(outer)

    def _create_header(self, parent):
        row = tk.Frame(parent, bg=Theme.BG_PRIMARY)
        row.pack(fill='x', pady=(0, 20))

        # Title + Karen script
        left = tk.Frame(row, bg=Theme.BG_PRIMARY)
        left.pack(side='left')

        tk.Label(left, text="S'gaw Karen Keyboard",
                 font=('Segoe UI', 21, 'bold'),
                 fg=Theme.TEXT, bg=Theme.BG_PRIMARY).pack(side='left')

        tk.Label(left, text="ကညီကျိာ်",
                 font=('Myanmar Text', 17),
                 fg=Theme.ORANGE, bg=Theme.BG_PRIMARY).pack(side='left', padx=(14, 0))

        # Version badge
        badge = tk.Frame(row, bg=Theme.BG_ELEVATED)
        badge.pack(side='right', pady=6)
        tk.Label(badge, text="v1.0",
                 font=('Segoe UI', 9),
                 fg=Theme.TEXT_MUTED, bg=Theme.BG_ELEVATED,
                 padx=10, pady=3).pack()

    def _create_status_card(self, parent):
        card = tk.Frame(parent, bg=Theme.BG_CARD,
                        highlightbackground=Theme.BORDER, highlightthickness=1)
        card.pack(fill='x', pady=(0, 18))

        inner = tk.Frame(card, bg=Theme.BG_CARD)
        inner.pack(fill='x', padx=22, pady=18)

        # --- Left: status display ---
        left = tk.Frame(inner, bg=Theme.BG_CARD)
        left.pack(side='left')

        dot_row = tk.Frame(left, bg=Theme.BG_CARD)
        dot_row.pack(anchor='w')

        self.status_dot = tk.Label(dot_row, text="●",
                                   font=('Segoe UI', 14),
                                   fg=Theme.RED, bg=Theme.BG_CARD)
        self.status_dot.pack(side='left')

        self.status_label = tk.Label(dot_row, text="Keyboard is OFF",
                                     font=('Segoe UI', 17, 'bold'),
                                     fg=Theme.RED, bg=Theme.BG_CARD)
        self.status_label.pack(side='left', padx=(10, 0))

        tk.Label(left,
                 text="Ctrl + Alt + Space  to toggle anywhere",
                 font=('Segoe UI', 10),
                 fg=Theme.TEXT_MUTED, bg=Theme.BG_CARD).pack(anchor='w', pady=(7, 0))

        # --- Right: toggle switch ---
        right = tk.Frame(inner, bg=Theme.BG_CARD)
        right.pack(side='right')

        sw_row = tk.Frame(right, bg=Theme.BG_CARD)
        sw_row.pack(anchor='center')

        self.toggle_switch = ToggleSwitch(sw_row, command=self._on_toggle_click)
        self.toggle_switch.pack(side='left')

        self.toggle_label = tk.Label(sw_row, text="OFF",
                                     font=('Segoe UI', 12, 'bold'),
                                     fg=Theme.TEXT_MUTED, bg=Theme.BG_CARD, width=4)
        self.toggle_label.pack(side='left', padx=(10, 0))

    def _create_keyboard_section(self, parent):
        # Header row
        hdr = tk.Frame(parent, bg=Theme.BG_PRIMARY)
        hdr.pack(fill='x', pady=(0, 10))

        tk.Label(hdr, text="Keyboard Layout",
                 font=('Segoe UI', 12, 'bold'),
                 fg=Theme.TEXT, bg=Theme.BG_PRIMARY).pack(side='left')

        legend = tk.Frame(hdr, bg=Theme.BG_PRIMARY)
        legend.pack(side='right')
        for color, text in [(Theme.GREEN, " Normal  "), (Theme.ORANGE, " Shift")]:
            tk.Label(legend, text="●", font=('Segoe UI', 9),
                     fg=color, bg=Theme.BG_PRIMARY).pack(side='left')
            tk.Label(legend, text=text, font=('Segoe UI', 9),
                     fg=Theme.TEXT_SUB, bg=Theme.BG_PRIMARY).pack(side='left')

        # Card
        kb_card = tk.Frame(parent, bg=Theme.BG_CARD,
                           highlightbackground=Theme.BORDER, highlightthickness=1)
        kb_card.pack(fill='both', expand=True)

        kb_center = tk.Frame(kb_card, bg=Theme.BG_CARD)
        kb_center.pack(expand=True, pady=14)

        rows = [('row1', 0), ('row2', 20), ('row3', 38), ('row4', 56)]
        for row_name, indent in rows:
            row_frame = tk.Frame(kb_center, bg=Theme.BG_CARD)
            row_frame.pack(anchor='w', padx=indent, pady=2)
            for label, karen, shift in KEYBOARD_LAYOUT[row_name]:
                key = KeyButton(row_frame, label, karen, shift, self.size_multiplier)
                key.pack(side='left', padx=2, pady=2)

    def _create_footer(self, parent):
        footer = tk.Frame(parent, bg=Theme.BG_PRIMARY)
        footer.pack(fill='x', pady=(16, 0))

        btn = dict(
            font=('Segoe UI', 10),
            fg=Theme.TEXT_SUB,
            bg=Theme.BG_ELEVATED,
            activebackground=Theme.BG_KEY_HOVER,
            activeforeground=Theme.TEXT,
            relief='flat', cursor='hand2',
            padx=14, pady=7,
        )

        left = tk.Frame(footer, bg=Theme.BG_PRIMARY)
        left.pack(side='left')
        tk.Button(left, text="About", command=self.show_about, **btn).pack(side='left', padx=(0, 8))
        tk.Button(left, text="Settings", command=self.show_settings, **btn).pack(side='left')

        tk.Button(footer, text="Minimize to Tray",
                  command=self.minimize_to_tray, **btn).pack(side='right')

        tk.Label(footer,
                 text="Made with love by Songnam Saraphai",
                 font=('Segoe UI', 9),
                 fg=Theme.TEXT_MUTED, bg=Theme.BG_PRIMARY).pack(pady=(10, 0))

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def _on_toggle_click(self):
        """Called by the toggle switch after it flips its own visual state."""
        active = self.keyboard_hook.toggle()
        self._apply_status(active, sync_switch=False)

    def update_status(self, active):
        """Called externally (e.g. hotkey) to sync all UI state."""
        self._apply_status(active, sync_switch=True)

    def _apply_status(self, active, sync_switch):
        if active:
            self.status_label.config(text="Keyboard is ON", fg=Theme.GREEN)
            self.status_dot.config(fg=Theme.GREEN)
            self.toggle_label.config(text="ON", fg=Theme.GREEN)
        else:
            self.status_label.config(text="Keyboard is OFF", fg=Theme.RED)
            self.status_dot.config(fg=Theme.RED)
            self.toggle_label.config(text="OFF", fg=Theme.TEXT_MUTED)

        if sync_switch:
            self.toggle_switch.set_active(active)

        if self.tray_icon:
            self.tray_icon.update_icon(active)

    def toggle_keyboard(self):
        """Legacy entry point kept for compatibility."""
        active = self.keyboard_hook.toggle()
        self._apply_status(active, sync_switch=True)

    # ------------------------------------------------------------------
    # Window management
    # ------------------------------------------------------------------

    def minimize_to_tray(self):
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    # ------------------------------------------------------------------
    # Dialogs
    # ------------------------------------------------------------------

    def _center_dialog(self, win, w, h):
        x = self.root.winfo_x() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

    def show_about(self):
        win = tk.Toplevel(self.root)
        win.title("About")
        win.configure(bg=Theme.BG_PRIMARY)
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)
        self._center_dialog(win, 400, 310)

        tk.Label(win, text="S'gaw Karen Keyboard",
                 font=('Segoe UI', 18, 'bold'),
                 fg=Theme.TEXT, bg=Theme.BG_PRIMARY).pack(pady=(30, 4))

        tk.Label(win, text="ကညီကျိာ်  —  K'nyaw Keyboard",
                 font=('Myanmar Text', 14),
                 fg=Theme.ORANGE, bg=Theme.BG_PRIMARY).pack()

        tk.Label(win, text="Version 1.0",
                 font=('Segoe UI', 10),
                 fg=Theme.TEXT_MUTED, bg=Theme.BG_PRIMARY).pack(pady=(4, 18))

        Divider(win).pack(fill='x', padx=30, pady=(0, 18))

        tk.Label(win,
                 text="S'gaw Karen Keyboard for Windows\n"
                      "Based on the official Kawthoolei layout\n"
                      "Ctrl + Alt + Space to toggle anywhere",
                 font=('Segoe UI', 11),
                 fg=Theme.TEXT_SUB, bg=Theme.BG_PRIMARY,
                 justify='center').pack()

        tk.Label(win, text="Made with love by Songnam Saraphai",
                 font=('Segoe UI', 9),
                 fg=Theme.TEXT_MUTED, bg=Theme.BG_PRIMARY).pack(side='bottom', pady=20)

    def show_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.configure(bg=Theme.BG_PRIMARY)
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)
        self._center_dialog(win, 420, 290)

        tk.Label(win, text="Settings",
                 font=('Segoe UI', 16, 'bold'),
                 fg=Theme.TEXT, bg=Theme.BG_PRIMARY).pack(pady=(24, 10), anchor='w', padx=30)

        Divider(win).pack(fill='x', padx=30, pady=(0, 18))

        options = tk.Frame(win, bg=Theme.BG_PRIMARY)
        options.pack(fill='x', padx=30)

        cb_style = dict(
            font=('Segoe UI', 11),
            fg=Theme.TEXT,
            bg=Theme.BG_PRIMARY,
            activebackground=Theme.BG_PRIMARY,
            activeforeground=Theme.TEXT,
            selectcolor=Theme.BG_ELEVATED,
        )

        auto_var = tk.BooleanVar(value=self.settings.is_auto_start_enabled())
        tk.Checkbutton(options, text="Start with Windows",
                       variable=auto_var, **cb_style).pack(anchor='w', pady=6)

        min_var = tk.BooleanVar(value=self.settings.get('start_minimized', False))
        tk.Checkbutton(options, text="Start minimized to tray",
                       variable=min_var, **cb_style).pack(anchor='w', pady=6)

        status_lbl = tk.Label(win, text="",
                              font=('Segoe UI', 10),
                              fg=Theme.GREEN, bg=Theme.BG_PRIMARY)
        status_lbl.pack(pady=(10, 0))

        btn_frame = tk.Frame(win, bg=Theme.BG_PRIMARY)
        btn_frame.pack(pady=16)

        def save():
            result = self.settings.set_auto_start(auto_var.get())
            self.settings.set('start_minimized', min_var.get())
            if result:
                status_lbl.config(text="Settings saved", fg=Theme.GREEN)
            else:
                status_lbl.config(text="Saved (auto-start may need admin rights)", fg=Theme.ORANGE)
            win.after(900, win.destroy)

        tk.Button(btn_frame, text="Save",
                  font=('Segoe UI', 11, 'bold'),
                  fg='#0d1117', bg=Theme.GREEN,
                  activebackground='#22c55e', activeforeground='#0d1117',
                  relief='flat', cursor='hand2',
                  padx=26, pady=8,
                  command=save).pack(side='left', padx=(0, 8))

        tk.Button(btn_frame, text="Cancel",
                  font=('Segoe UI', 11),
                  fg=Theme.TEXT_SUB, bg=Theme.BG_ELEVATED,
                  activebackground=Theme.BG_KEY_HOVER, activeforeground=Theme.TEXT,
                  relief='flat', cursor='hand2',
                  padx=26, pady=8,
                  command=win.destroy).pack(side='left')

    def run(self):
        self.root.mainloop()
