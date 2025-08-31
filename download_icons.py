#!/usr/bin/env python3
"""
Download Tabler Icons for Tortoise Care Touch
Fetches specific icons needed for the application
"""

import os
import requests
import sys

# Base URL for Tabler Icons on GitHub
TABLER_BASE_URL = "https://raw.githubusercontent.com/tabler/tabler-icons/master/icons"

# Icons we need for our application
REQUIRED_ICONS = [
    # Settings icons
    'users.svg',
    'user.svg',
    'settings.svg', 
    'database.svg',
    'wifi.svg',
    
    # Health icons
    'heart.svg',
    'stethoscope.svg',
    'alert-triangle.svg',
    'phone.svg',
    'clipboard.svg',
    'pill.svg',
    'exclamation-triangle.svg',
    
    # Navigation icons
    'home.svg',
    'arrow-left.svg',
    'info-circle.svg',
    
    # Feature icons
    'apple.svg',          # Food/feeding
    'leaf.svg',           # Plants
    'trending-up.svg',    # Growth
    'calendar.svg',       # Reminders
    'bug.svg',            # Tortoise (closest available)
]

def download_icon(icon_name, icons_dir):
    """Download a single icon from Tabler Icons"""
    url = f"{TABLER_BASE_URL}/{icon_name}"
    icon_path = os.path.join(icons_dir, icon_name)
    
    try:
        print(f"Downloading {icon_name}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(icon_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✓ {icon_name} downloaded successfully")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to download {icon_name}: {e}")
        return False
    except Exception as e:
        print(f"✗ Error saving {icon_name}: {e}")
        return False

def main():
    """Download all required icons"""
    # Get project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(project_dir, 'icons')
    
    # Create icons directory if it doesn't exist
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        print(f"Created icons directory: {icons_dir}")
    
    print("Downloading Tabler Icons for Tortoise Care Touch...")
    print(f"Target directory: {icons_dir}")
    print("-" * 50)
    
    # Download all required icons
    successful = 0
    total = len(REQUIRED_ICONS)
    
    for icon_name in REQUIRED_ICONS:
        if download_icon(icon_name, icons_dir):
            successful += 1
    
    print("-" * 50)
    print(f"Download complete: {successful}/{total} icons downloaded")
    
    if successful == total:
        print("✓ All icons downloaded successfully!")
        
        # Create a simple README for the icons folder
        readme_path = os.path.join(icons_dir, 'README.md')
        with open(readme_path, 'w') as f:
            f.write("# Tabler Icons\n\n")
            f.write("This folder contains SVG icons from Tabler Icons (https://tabler.io/icons)\n")
            f.write("Licensed under MIT License\n\n")
            f.write("Icons downloaded for Tortoise Care Touch application.\n")
        
        print("✓ Created README.md in icons folder")
        
    else:
        print(f"⚠ {total - successful} icons failed to download")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())