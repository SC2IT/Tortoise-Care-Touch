#!/usr/bin/env python3
"""
Test script for Tabler Icons integration
"""

import os
from pathlib import Path

# Replicate IconManager constants for testing without importing Kivy
ICONS_PATH = os.path.join(os.path.dirname(__file__), 'icons')
ICON_MAP = {
    'users': 'users.png',
    'user': 'users.png', 
    'settings': 'settings.png',
    'database': 'database.png',
    'wifi': 'wifi.png',
    'heart': 'heart.png',
    'medical': 'stethoscope.png',
    'emergency': 'alert-triangle.png',
    'phone': 'phone.png',
    'home': 'heart.png',
    'food': 'heart.png',
    'plant': 'heart.png',
    'growth': 'heart.png',
    'calendar': 'heart.png',
    'clipboard': 'heart.png',
    'pill': 'stethoscope.png',
    'warning': 'alert-triangle.png',
    'tortoise': 'bug.png',
    'back': 'arrow-left.png',
    'info': 'heart.png'
}

def get_icon_path(icon_name):
    """Get the full path to an icon file"""
    if icon_name in ICON_MAP:
        return os.path.join(ICONS_PATH, ICON_MAP[icon_name])
    return None

def test_icon_paths():
    """Test that icon files exist and paths are correct"""
    print("Testing Tabler Icons integration...")
    print("="*50)
    
    # Test icons directory exists
    if os.path.exists(ICONS_PATH):
        print(f"OK Icons directory found: {ICONS_PATH}")
    else:
        print(f"ERROR Icons directory not found: {ICONS_PATH}")
        return False
    
    # Test individual icon files
    success_count = 0
    for icon_name, file_name in ICON_MAP.items():
        icon_path = get_icon_path(icon_name)
        if icon_path and os.path.exists(icon_path):
            file_size = os.path.getsize(icon_path)
            print(f"OK {icon_name:12} -> {file_name:20} ({file_size} bytes)")
            success_count += 1
        else:
            print(f"ERROR {icon_name:12} -> {file_name:20} (NOT FOUND)")
    
    print("="*50)
    print(f"Icons found: {success_count}/{len(ICON_MAP)}")
    
    if success_count == len(ICON_MAP):
        print("SUCCESS All icons are available!")
        return True
    else:
        print("WARNING Some icons are missing")
        return False

def test_icon_widget_creation():
    """Test creating icon widgets (simulated)"""
    print("\nTesting icon widget creation...")
    print("="*50)
    
    test_icons = ['users', 'settings', 'database', 'heart', 'emergency']
    
    for icon_name in test_icons:
        icon_path = get_icon_path(icon_name)
        if icon_path and os.path.exists(icon_path):
            print(f"OK {icon_name:12} -> Ready for Image widget")
        else:
            print(f"WARNING {icon_name:12} -> Would use text fallback")
    
    print("="*50)

if __name__ == '__main__':
    print("Tortoise Care Touch - Icon Integration Test")
    print("="*50)
    
    path_test = test_icon_paths()
    test_icon_widget_creation()
    
    if path_test:
        print("\nSUCCESS Icon integration is ready!")
        print("\nNext steps:")
        print("1. Update all UI screens to use IconManager")
        print("2. Test on Raspberry Pi display")
        print("3. Adjust icon sizes if needed")
    else:
        print("\nERROR Icon integration needs fixing")
        print("Run: python convert_icons.py")