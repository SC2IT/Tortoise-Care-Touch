#!/usr/bin/env python3
"""
Installation and setup script for Tortoise Care Touch
Run this script to set up the application on your Raspberry Pi
"""

import os
import sys
import subprocess
import sqlite3

def check_python_version():
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def setup_directories():
    print("Setting up directories...")
    
    # Create photo directories
    photo_dirs = [
        'photos/tortoises',
        'photos/plants/leaves',
        'photos/plants/flowers',
        'photos/plants/full',
        'photos/growth',
        'data/backups'
    ]
    
    for dir_path in photo_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")

def initialize_database():
    print("Initializing database...")
    try:
        from database.db_manager import DatabaseManager
        db = DatabaseManager()
        db.initialize_database()
        db.close()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

def create_desktop_entry():
    """Create a desktop entry for easy access on Raspberry Pi Desktop"""
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=Tortoise Care Touch
Comment=Touch-screen tortoise care tracking and monitoring application
Exec=python3 /home/pi/tortoise-care-touch/main.py
Icon=/home/pi/tortoise-care-touch/icon.png
Terminal=false
Categories=Education;Science;
"""
    
    desktop_dir = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop_dir):
        desktop_file = os.path.join(desktop_dir, "TortoiseCareTouch.desktop")
        with open(desktop_file, 'w') as f:
            f.write(desktop_content)
        os.chmod(desktop_file, 0o755)
        print("✓ Desktop shortcut created")

def setup_autostart():
    """Set up the application to start automatically (optional)"""
    autostart_dir = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_dir, exist_ok=True)
    
    autostart_content = """[Desktop Entry]
Type=Application
Name=Tortoise Care Touch
Exec=python3 /home/pi/tortoise-care-touch/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
    
    autostart_file = os.path.join(autostart_dir, "tortoise-care-touch.desktop")
    
    response = input("Would you like the application to start automatically on boot? (y/n): ")
    if response.lower() == 'y':
        with open(autostart_file, 'w') as f:
            f.write(autostart_content)
        print("✓ Autostart configured")
    else:
        print("⚬ Skipped autostart configuration")

def check_display():
    """Check if running in a desktop environment"""
    if os.environ.get('DISPLAY'):
        print("✓ Display environment detected")
        return True
    else:
        print("⚬ No display environment detected (headless mode)")
        return False

def main():
    print("=== Tortoise Care Application Setup ===\n")
    
    check_python_version()
    install_dependencies()
    setup_directories()
    initialize_database()
    
    if check_display():
        create_desktop_entry()
        setup_autostart()
    
    print("\n=== Setup Complete! ===")
    print("Tortoise Care Touch is now ready to use.")
    print("\nTo start the application:")
    print("  python3 main.py")
    print("\nFor Pi Touch Display 2 optimization:")
    print("1. Application auto-detects portrait/landscape orientation")
    print("2. UI adapts automatically to screen rotation")
    print("3. Touch calibration should work out of the box")
    print("\nNext steps:")
    print("- Add your tortoises in the application")
    print("- Configure Adafruit.IO settings for habitat monitoring")
    print("- Set up photo import folder for growth tracking")
    print("- Test orientation changes by rotating your display")

if __name__ == "__main__":
    main()