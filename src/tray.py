"""
System Tray Module
Handles the system tray icon and menu.
"""

import pystray
from PIL import Image, ImageDraw
import threading
import os
import sys


def get_icon_path():
    """Get the path to the icon file."""
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        base_dir = sys._MEIPASS
    else:
        # Running as script
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'S_gawKeyboardApp.ico')


class TrayIcon:
    """System tray icon handler."""
    
    def __init__(self, on_toggle=None, on_show=None, on_exit=None, on_about=None, on_settings=None):
        self.on_toggle = on_toggle
        self.on_show = on_show
        self.on_exit = on_exit
        self.on_about = on_about
        self.on_settings = on_settings
        self.icon = None
        self.is_active = False
        self._icon_image = None
        self._load_icon()
        
    def _load_icon(self):
        """Load the custom icon file."""
        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self._icon_image = Image.open(icon_path)
                # Resize for tray (64x64)
                self._icon_image = self._icon_image.resize((64, 64), Image.Resampling.LANCZOS)
            else:
                self._icon_image = None
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")
            self._icon_image = None
        
    def create_icon_image(self, active=False):
        """Return the icon image (with optional overlay for status)."""
        if self._icon_image:
            # Use the custom icon
            return self._icon_image.copy()
        
        # Fallback: create a simple icon
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw a rounded rectangle background
        bg_color = (78, 204, 163) if active else (249, 115, 22)
        draw.rounded_rectangle([4, 4, size-4, size-4], radius=10, fill=bg_color)
        
        # Draw "K" for Karen
        draw.text((size//2, size//2), "K", fill='white', anchor='mm')
        
        return image
        
    def update_icon(self, active):
        """Update the icon to reflect active state."""
        self.is_active = active
        if self.icon:
            self.icon.icon = self.create_icon_image(active)
            status = "ON" if active else "OFF"
            self.icon.title = f"S'gaw Karen Keyboard - {status}"
            
    def _create_menu(self):
        """Create the tray menu."""
        return pystray.Menu(
            pystray.MenuItem("Show Window", self._on_show, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Toggle Keyboard (Ctrl+Alt+Space)", self._on_toggle),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("About", self._on_about),
            pystray.MenuItem("Settings", self._on_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._on_exit_click)
        )
        
    def _on_show(self, icon, item):
        """Handle show window click."""
        if self.on_show:
            self.on_show()
            
    def _on_toggle(self, icon, item):
        """Handle toggle click."""
        if self.on_toggle:
            self.on_toggle()
    
    def _on_about(self, icon, item):
        """Handle about click."""
        if self.on_about:
            self.on_about()
    
    def _on_settings(self, icon, item):
        """Handle settings click."""
        if self.on_settings:
            self.on_settings()
            
    def _on_exit_click(self, icon, item):
        """Handle exit click."""
        self.stop()
        if self.on_exit:
            self.on_exit()
            
    def start(self):
        """Start the tray icon in a separate thread."""
        self.icon = pystray.Icon(
            "sgaw_karen_keyboard",
            self.create_icon_image(False),
            "S'gaw Karen Keyboard - OFF",
            menu=self._create_menu()
        )
        
        # Run in a separate thread
        thread = threading.Thread(target=self.icon.run, daemon=True)
        thread.start()
        
    def stop(self):
        """Stop the tray icon."""
        if self.icon:
            self.icon.stop()
