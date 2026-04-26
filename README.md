# S'gaw Karen Keyboard 🇲🇲

**ကညီကျိာ် — K'nyaw Keyboard**

The **first S'gaw Karen keyboard** for Windows! Type in the Karen language using the official KNU (Karen National Union) keyboard layout.

![Keyboard Layout](docs/keyboard-layout.png)

## ✨ Features

- 🎹 **Full KNU Layout** - Official Karen National Union keyboard mapping
- ⌨️ **Global Hotkey** - Press `Ctrl+Alt+K` to toggle anywhere
- 🖥️ **Visual Keyboard** - See the layout with all characters
- 📊 **System Tray** - Runs quietly in the background
- 🚀 **Auto-Start** - Optional Windows startup
- 📦 **Standalone** - Single .exe file, no installation needed

## 🚀 Quick Start

### Option 1: Download the .exe (Recommended)

1. Download `SgawKarenKeyboard.exe` from [Releases](releases/)
2. Double-click to run
3. Press `Ctrl+Alt+K` to toggle the keyboard

### Option 2: Run from Source

```powershell
# Clone or download this repository
cd "Sgaw Karen Keyboard"

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Option 3: Build Your Own .exe

```powershell
# Install dependencies
pip install -r requirements.txt

# Build
python build.py
```

The .exe will be in the `dist/` folder.

## ⌨️ How to Use

1. **Start the keyboard** - Run the application
2. **Toggle ON/OFF** - Press `Ctrl+Alt+K` (works in any app!)
3. **Type normally** - Your keystrokes become Karen characters

### Keyboard Layout

| Key | Normal | Shift |
|-----|--------|-------|
| q | ဆ (hsa) | ၐ |
| w | တ (ta) | ဋ |
| e | န (na) | ဏ |
| r | မ (ma) | ္ |
| t | အ (a) | ဍ |
| y | ပ (pa) | ၑ |
| u | က (ka) | ၵ |
| i | င (nga) | ဎ |
| o | ော (aw) | ဩ |
| p | စ (sa) | ဿ |

*See the application for the full layout*

## 🎨 Character Categories

### Consonants (25 letters)
က ခ ဂ ဃ င စ ဆ ဇ ည ဋ ဌ ဍ ဎ ဏ တ ထ ဒ ဓ န ပ ဖ ဘ မ ယ သ

### Vowels (9 marks)
ါ ာ ိ ီ ု ူ ေ ဲ ော

### Medials (5 marks)
ျ ြ ွ ှ ္

### Tones (6 marks)
့ း ံ ္ ့် ျ

## 💻 Technical Details

- **Language**: Python 3.8+
- **GUI**: tkinter (built-in)
- **Keyboard**: pynput
- **Tray**: pystray
- **Unicode**: Myanmar block (U+1000-U+109F)

## 📁 Project Structure

```
Sgaw Karen Keyboard/
├── main.py              # Entry point
├── src/
│   ├── __init__.py
│   ├── mappings.py      # KNU keyboard mappings
│   ├── keyboard_hook.py # Keyboard interception
│   ├── gui.py           # Main window
│   ├── settings.py      # Settings persistence
│   └── tray.py          # System tray icon
├── requirements.txt
├── build.py             # PyInstaller build script
└── README.md
```

## 🤝 Contributing

Contributions are welcome! This is the first Karen keyboard for Windows, and there's always room for improvement.

## 📜 License

MIT License - Feel free to use and modify.

## ❤️ Credits

- **Developer**: Songnam Saraphai
- **Keyboard Layout**: Based on official KNU S'gaw Karen layout
- **Unicode**: Myanmar Unicode Consortium


