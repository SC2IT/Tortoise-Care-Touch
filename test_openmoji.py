#!/usr/bin/env python3
"""
Test OpenMoji icon integration
"""

import os
from pathlib import Path
from utils.openmoji_icons import OpenMojiIconManager

def test_icons():
    """Test that all icons are downloaded and accessible"""
    manager = OpenMojiIconManager()
    icons_dir = Path(__file__).parent / 'icons'
    
    print("OpenMoji Icons Test")
    print("=" * 50)
    
    # Test icons directory exists
    if icons_dir.exists():
        print(f"OK Icons directory found: {icons_dir}")
    else:
        print(f"ERROR Icons directory not found: {icons_dir}")
        return False
    
    # Count PNG files
    png_files = list(icons_dir.glob('*.png'))
    print(f"OK Found {len(png_files)} PNG icon files")
    
    # Test specific essential icons
    essential_icons = [
        'settings', 'home', 'user', 'users', 'tortoise',
        'heart', 'medical', 'emergency', 'phone', 'calendar',
        'camera', 'chart', 'clipboard', 'thermometer', 'droplet'
    ]
    
    print("\nTesting essential icons:")
    print("-" * 30)
    
    missing_icons = []
    for icon_name in essential_icons:
        icon_path = manager.get_icon_path(icon_name)
        if icon_path and os.path.exists(icon_path):
            file_size = os.path.getsize(icon_path)
            print(f"OK {icon_name:15} -> {file_size:,} bytes")
        else:
            print(f"ERROR {icon_name:15} -> MISSING")
            missing_icons.append(icon_name)
    
    print("=" * 50)
    
    if missing_icons:
        print(f"WARNING {len(missing_icons)} icons missing: {', '.join(missing_icons)}")
        return False
    else:
        print(f"SUCCESS All {len(essential_icons)} essential icons available!")
        print("\nIcon integration ready for Kivy UI!")
        return True

if __name__ == '__main__':
    test_icons()