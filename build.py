# S'gaw Karen Keyboard - Build Script
# ကညီကျိာ် — K'nyaw Keyboard
#
# This script builds the standalone .exe file using PyInstaller
#
# Usage: python build.py

import os
import sys
import subprocess
import shutil

def main():
    print("=" * 60)
    print("  S'gaw Karen Keyboard - Build Script")
    print("  ကညီကျိာ် — K'nyaw Keyboard")
    print("=" * 60)
    print()
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
    
    # Check dependencies
    print("\n--- Checking dependencies ---")
    deps = ['keyboard', 'pystray', 'PIL']
    for dep in deps:
        try:
            __import__(dep)
            print(f"✓ {dep} found")
        except ImportError:
            print(f"✗ {dep} not found. Installing dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            break
    
    # Clean previous builds
    print("\n--- Cleaning previous builds ---")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ Removed {folder}/")
    
    for f in os.listdir('.'):
        if f.endswith('.spec'):
            os.remove(f)
            print(f"✓ Removed {f}")
    
    # Use custom icon
    icon_path = os.path.join(script_dir, 'S_gawKeyboardApp.ico')
    if not os.path.exists(icon_path):
        print(f"\n⚠ Warning: Icon not found at {icon_path}")
        print("  Creating default icon...")
        create_icon(icon_path)
    else:
        print(f"\n✓ Using custom icon: {icon_path}")
    
    # Build with PyInstaller
    print("\n--- Building with PyInstaller ---")
    pyinstaller_args = [
        'main.py',
        '--name=SgawKarenKeyboard',
        '--onefile',                    # Single .exe file
        '--windowed',                   # No console window
        '--clean',                      # Clean cache
        f'--icon={icon_path}',          # Application icon
        '--add-data=src;src',           # Include src folder
        f'--add-data={icon_path};.',    # Include icon file in bundle
    ]
    
    # Add hidden imports that PyInstaller might miss
    hidden_imports = [
        'keyboard',
        'pystray._win32',
        'PIL._tkinter_finder',
    ]
    for imp in hidden_imports:
        pyinstaller_args.append(f'--hidden-import={imp}')
    
    print(f"Running: pyinstaller {' '.join(pyinstaller_args)}")
    print()
    
    subprocess.check_call([sys.executable, '-m', 'PyInstaller'] + pyinstaller_args)
    
    # Check if build succeeded
    exe_path = os.path.join(script_dir, 'dist', 'SgawKarenKeyboard.exe')
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print()
        print("=" * 60)
        print("  BUILD SUCCESSFUL!")
        print("=" * 60)
        print(f"\n  Output: {exe_path}")
        print(f"  Size: {size_mb:.1f} MB")
        print()
        print("  You can now distribute SgawKarenKeyboard.exe")
        print("  No installation or dependencies needed!")
        print()
    else:
        print()
        print("=" * 60)
        print("  BUILD FAILED!")
        print("=" * 60)
        print("  Check the error messages above.")
        sys.exit(1)


def create_icon(path):
    """Create a simple icon with Karen text."""
    from PIL import Image, ImageDraw, ImageFont
    
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = []
    
    for size in sizes:
        img = Image.new('RGBA', size, (74, 204, 163, 255))  # Green background
        draw = ImageDraw.Draw(img)
        
        # Draw "က" (Karen letter) or "K" if font not available
        try:
            font_size = int(size[0] * 0.7)
            font = ImageFont.truetype("C:\\Windows\\Fonts\\mmrtext.ttf", font_size)
            text = "က"
        except:
            font_size = int(size[0] * 0.6)
            try:
                font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            text = "K"
        
        # Center the text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2 - bbox[1]
        
        draw.text((x, y), text, fill=(26, 26, 46, 255), font=font)  # Dark text
        images.append(img)
    
    # Save as ICO
    images[0].save(path, format='ICO', sizes=[(s[0], s[1]) for s in sizes], 
                   append_images=images[1:])


if __name__ == "__main__":
    main()
