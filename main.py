"""
S'gaw Karen Keyboard - Main Entry Point
ကညီကျိာ် — K'nyaw Keyboard

The First S'gaw Karen Keyboard for Windows!
Based on the official KNU (Karen National Union) keyboard layout.

Usage:
  python main.py

Controls:
  Ctrl+Alt+Space - Toggle keyboard on/off (works anywhere)
  
Author: Songnam Saraphai
Version: 1.0.0
"""

import sys
import os
import threading
import tkinter as tk
from tkinter import messagebox

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.keyboard_hook import KarenKeyboardHook
from src.settings import Settings
from src.tray import TrayIcon
from src.gui import MainWindow


def check_single_instance():
    """Check if another instance is already running."""
    import socket
    try:
        # Try to bind to a specific port - if it fails, another instance is running
        global _instance_socket
        _instance_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _instance_socket.bind(('127.0.0.1', 47391))  # Random port for this app
        return True
    except socket.error:
        return False


def show_first_launch_dialog(root, settings):
    """Show first launch welcome dialog."""
    result = messagebox.askyesno(
        "Welcome to S'gaw Karen Keyboard!",
        "ကညီကျိာ် — Welcome!\n\n"
        "This is the first S'gaw Karen Keyboard for Windows!\n\n"
        "Would you like this keyboard to start automatically\n"
        "when Windows starts?\n\n"
        "(You can change this later in Settings)",
        parent=root
    )
    
    if result:
        settings.set_auto_start(True)
        messagebox.showinfo(
            "Auto-Start Enabled",
            "Great! The keyboard will now start automatically.\n\n"
            "Tips:\n"
            "• Press Ctrl+Alt+Space to toggle the keyboard\n"
            "• This works in any application!\n"
            "• Close this window to minimize to the system tray",
            parent=root
        )
    else:
        messagebox.showinfo(
            "Quick Start",
            "No problem! You can enable this later in Settings.\n\n"
            "Tips:\n"
            "• Press Ctrl+Alt+Space to toggle the keyboard\n"
            "• This works in any application!\n"
            "• Close this window to minimize to the system tray",
            parent=root
        )
    
    settings.set_first_launch_done()


def main():
    """Main entry point."""
    # Check single instance
    if not check_single_instance():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Already Running",
            "S'gaw Karen Keyboard is already running!\n\n"
            "Look for the icon in your system tray (near the clock)."
        )
        root.destroy()
        return
    
    import sys
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("Starting S'gaw Karen Keyboard...")
    print("Karen Keyboard - K'nyaw Keyboard")
    print("-" * 40)
    
    # Initialize components
    settings = Settings()
    keyboard_hook = KarenKeyboardHook()
    
    # Create GUI first (needed for dialogs and as root)
    main_window = MainWindow(keyboard_hook, settings, None)
    main_window.create_window()
    
    # Set up status change callback (runs on hotkey press from any thread)
    def on_status_change(active):
        # Schedule GUI update on main thread
        try:
            main_window.root.after(0, lambda: main_window.update_status(active))
            # Also update tray icon
            if main_window.tray_icon:
                main_window.tray_icon.update_icon(active)
        except:
            pass
    
    keyboard_hook.on_status_change = on_status_change
    
    # Create tray icon (needs root window reference for showing/hiding)
    def toggle_callback():
        active = keyboard_hook.toggle()
        main_window.update_status(active)
        return active
        
    def show_callback():
        main_window.show_window()
        
    def exit_callback():
        keyboard_hook.stop()
        main_window.root.quit()
        main_window.root.destroy()
    
    def about_callback():
        main_window.show_window()
        main_window.root.after(100, main_window.show_about)
    
    def settings_callback():
        main_window.show_window()
        main_window.root.after(100, main_window.show_settings)
    
    tray_icon = TrayIcon(toggle_callback, show_callback, exit_callback, about_callback, settings_callback)
    main_window.tray_icon = tray_icon
    
    # Start tray icon
    tray_icon.start()
    
    # Start keyboard hook
    keyboard_hook.start()
    print("✓ Keyboard hook started")
    print("  Press Ctrl+Alt+Space to toggle")
    
    # Check for first launch
    if settings.is_first_launch():
        main_window.root.after(500, lambda: show_first_launch_dialog(main_window.root, settings))
    
    # Start minimized if setting enabled
    if settings.get('start_minimized', False):
        main_window.root.withdraw()
        print("✓ Started minimized in system tray")
    else:
        print("✓ GUI window opened")
    
    print("-" * 40)
    print("S'gaw Karen Keyboard is ready!")
    print("Type in any application and your text will be converted to Karen script.")
    
    # Update initial status
    main_window.update_status(keyboard_hook.is_active())
    
    # Run main loop
    try:
        main_window.run()
    except KeyboardInterrupt:
        pass
    finally:
        print("\nShutting down...")
        keyboard_hook.stop()
        tray_icon.stop()
        print("Goodbye! ကညီကျိာ်")


if __name__ == "__main__":
    main()
