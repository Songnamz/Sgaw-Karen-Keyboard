"""
Settings Module
Handles application settings persistence.
"""

import json
import os
from pathlib import Path


class Settings:
    """Manages application settings."""
    
    DEFAULT_SETTINGS = {
        'auto_start': False,
        'start_minimized': False,
        'first_launch_done': False,
        'hotkey': 'ctrl+alt+space',
        'theme': 'dark',
    }
    
    def __init__(self):
        self.settings_dir = Path(os.environ.get('APPDATA', '')) / 'SgawKarenKeyboard'
        self.settings_file = self.settings_dir / 'settings.json'
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load()
        
    def load(self):
        """Load settings from file."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    self.settings.update(saved)
        except Exception as e:
            print(f"Error loading settings: {e}")
            
    def save(self):
        """Save settings to file."""
        try:
            self.settings_dir.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def get(self, key, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)
        
    def set(self, key, value):
        """Set a setting value and save."""
        self.settings[key] = value
        self.save()
        
    def is_first_launch(self):
        """Check if this is the first launch."""
        return not self.settings.get('first_launch_done', False)
        
    def set_first_launch_done(self):
        """Mark first launch as complete."""
        self.set('first_launch_done', True)
        
    def set_auto_start(self, enabled):
        """Set auto-start on Windows boot."""
        import winreg
        import sys
        
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "SgawKarenKeyboard"
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, 
                                winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE)
            
            if enabled:
                # Get the executable path
                if getattr(sys, 'frozen', False):
                    # Running as compiled exe
                    exe_path = f'"{sys.executable}"'
                else:
                    # Running as script
                    script_path = os.path.abspath(sys.argv[0])
                    exe_path = f'"{sys.executable}" "{script_path}"'
                    
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
                print(f"✓ Auto-start enabled: {exe_path}")
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                    print("✓ Auto-start disabled")
                except FileNotFoundError:
                    print("✓ Auto-start was already disabled")
                    pass
                    
            winreg.CloseKey(key)
            self.settings['auto_start'] = enabled
            self.save()
            return True
            
        except Exception as e:
            print(f"Error setting auto-start: {e}")
            return False
            
    def is_auto_start_enabled(self):
        """Check if auto-start is enabled in registry."""
        import winreg
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_READ)
            winreg.QueryValueEx(key, "SgawKarenKeyboard")
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False
