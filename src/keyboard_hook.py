"""
Keyboard Hook Module
Handles low-level keyboard interception and character substitution.
Uses the 'keyboard' library for Windows which properly supports key suppression.
"""

import keyboard
import threading
import time
import ctypes
from .mappings import NORMAL_MAPPINGS, SHIFT_MAPPINGS

# Windows API for checking key state
user32 = ctypes.windll.user32
VK_SHIFT = 0x10
VK_LSHIFT = 0xA0
VK_RSHIFT = 0xA1

def is_shift_pressed():
    """Check if Shift is currently pressed using Windows API."""
    return (user32.GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0


class KarenKeyboardHook:
    """Handles keyboard hooking and Karen character substitution."""
    
    def __init__(self, on_status_change=None):
        self.active = False
        self.on_status_change = on_status_change
        self._processing = False
        self._lock = threading.Lock()
        
    def start(self):
        """Start the keyboard hook."""
        # Register the toggle hotkey
        keyboard.add_hotkey('ctrl+alt+space', self._toggle_from_hotkey, suppress=True)
        
        # Use a global hook to intercept all keys
        keyboard.hook(self._on_key_event, suppress=True)
        print("Keyboard hook started - Ctrl+Alt+Space to toggle")
        
    def stop(self):
        """Stop the keyboard hook."""
        try:
            keyboard.unhook_all()
        except:
            pass
            
    def toggle(self):
        """Toggle the Karen keyboard on/off."""
        self.active = not self.active
        status = "ON" if self.active else "OFF"
        print(f"Karen Keyboard: {status}")
        if self.on_status_change:
            try:
                self.on_status_change(self.active)
            except:
                pass
        return self.active
        
    def _toggle_from_hotkey(self):
        """Toggle from hotkey press."""
        self.toggle()
        
    def set_active(self, active):
        """Set the keyboard active state."""
        self.active = active
        if self.on_status_change:
            self.on_status_change(self.active)
            
    def is_active(self):
        """Check if the keyboard is currently active."""
        return self.active
            
    def _on_key_event(self, event):
        """Handle key events."""
        # Only process key down events
        if event.event_type != 'down':
            return True
            
        # If not active, let key through
        if not self.active:
            return True
        
        # Prevent re-entry
        with self._lock:
            if self._processing:
                return True
        
        # Ignore modifier keys themselves
        if event.name in ('shift', 'ctrl', 'alt', 'left shift', 'right shift', 
                          'left ctrl', 'right ctrl', 'left alt', 'right alt',
                          'caps lock', 'tab', 'enter', 'backspace', 'delete',
                          'home', 'end', 'page up', 'page down', 'insert',
                          'up', 'down', 'left', 'right', 'escape',
                          'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 
                          'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
                          'print screen', 'scroll lock', 'pause',
                          'num lock', 'space', 'windows', 'left windows', 'right windows'):
            return True
            
        try:
            # Check if Shift is held down using Windows API (more reliable)
            shift_held = is_shift_pressed()
            
            karen_char = None
            
            # Handle single character keys (letters and symbols)
            if len(event.name) == 1:
                char = event.name
                char_lower = char.lower()
                
                if shift_held:
                    # Shift is held - check shift mappings for letters
                    if char_lower in SHIFT_MAPPINGS:
                        karen_char = SHIFT_MAPPINGS[char_lower]
                    # Also check if the symbol itself is in shift mappings
                    elif char in SHIFT_MAPPINGS:
                        karen_char = SHIFT_MAPPINGS[char]
                else:
                    # No shift - check normal mappings
                    if char_lower in NORMAL_MAPPINGS:
                        karen_char = NORMAL_MAPPINGS[char_lower]
                    elif char in NORMAL_MAPPINGS:
                        karen_char = NORMAL_MAPPINGS[char]
            else:
                # Multi-character key names (like symbols)
                if event.name in SHIFT_MAPPINGS:
                    karen_char = SHIFT_MAPPINGS[event.name]
                elif event.name in NORMAL_MAPPINGS:
                    karen_char = NORMAL_MAPPINGS[event.name]
                
            # Check if we have a mapping
            if karen_char is not None:
                # Send the Karen character
                with self._lock:
                    self._processing = True
                
                def send_char():
                    try:
                        time.sleep(0.005)  # Small delay
                        keyboard.write(karen_char)
                    except Exception as e:
                        print(f"Error sending char: {e}")
                    finally:
                        with self._lock:
                            self._processing = False
                        
                threading.Thread(target=send_char, daemon=True).start()
                
                # Block the original key
                return False
                
        except Exception as e:
            print(f"Error in key handler: {e}")
            with self._lock:
                self._processing = False
            
        return True
