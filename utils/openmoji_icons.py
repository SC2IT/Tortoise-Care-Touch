"""
OpenMoji Icon Manager for Tortoise Care Touch
Downloads and manages PNG icons from OpenMoji
"""

import os
import requests
from pathlib import Path

class OpenMojiIconManager:
    """Manages OpenMoji icons for the application"""
    
    def __init__(self):
        self.icons_dir = Path(__file__).parent.parent / 'icons'
        self.icons_dir.mkdir(exist_ok=True)
        
        # OpenMoji icon mapping - essential icons for Tortoise Care Touch
        self.icon_map = {
            # Basic UI & System
            'settings': '2699',      # ⚙️ gear
            'back': '2190',          # ← leftwards arrow  
            'home': '1F3E0',         # 🏠 house
            'info': '2139',          # ℹ️ information
            'x': '274C',             # ❌ cross mark
            'search': '1F50D',       # 🔍 magnifying glass
            
            # Users & People
            'user': '1F464',         # 👤 bust in silhouette
            'users': '1F465',        # 👥 busts in silhouette
            
            # Health & Care System
            'heart': '2764',         # ❤️ red heart
            'medical': '1FA7A',      # 🩺 stethoscope
            'pill': '1F48A',         # 💊 pill
            'emergency': '26A0',     # ⚠️ warning
            'phone': '1F4DE',        # 📞 telephone receiver
            'clipboard': '1F4CB',    # 📋 clipboard - health records
            'chart': '1F4CA',        # 📊 bar chart - health data
            'notes': '1F4DD',        # 📝 memo - care notes
            
            # Growth Tracking & Photos
            'camera': '1F4F7',       # 📷 camera
            'ruler': '1F4CF',        # 📏 straight ruler
            'scale': '2696',         # ⚖️ balance scale
            'trending-up': '1F4C8',  # 📈 chart increasing
            
            # Environmental Monitoring (Adafruit.IO)
            'thermometer': '1F321',  # 🌡️ thermometer
            'droplet': '1F4A7',      # 💧 droplet
            'activity': '1F4F6',     # 📶 antenna bars (sensor connectivity)
            'bar-chart': '1F4CA',    # 📊 bar chart (same as chart)
            
            # Care Reminders & Scheduling
            'calendar': '1F4C5',     # 📅 calendar
            'clock': '23F0',         # ⏰ alarm clock
            'bell': '1F514',         # 🔔 bell
            'check': '2705',         # ✅ check mark button
            
            # Food & Plant Database
            'tortoise': '1F422',     # 🐢 turtle
            'apple': '1F34E',        # 🍎 red apple
            'leaf': '1F343',         # 🍃 falling leaves
            'plant': '1F331',        # 🌱 seedling
            'salad': '1F957',        # 🥗 green salad
            
            # Navigation & Actions
            'plus': '2795',          # ➕ plus
            'edit': '270F',          # ✏️ pencil
            'trash': '1F5D1',        # 🗑️ wastebasket
            'save': '1F4BE',         # 💾 floppy disk
            'upload': '1F4E4',       # 📤 outbox tray
            'download': '1F4E5',     # 📥 inbox tray
            
            # Data & Technology
            'database': '1F4BE',     # 💾 floppy disk (same as save)
            'wifi': '1F4F6',         # 📶 antenna bars (same as activity)
        }
    
    def get_openmoji_url(self, hex_code, variant='color'):
        """Get OpenMoji download URL for a hex code"""
        # OpenMoji API uses uppercase hex codes
        hex_code = hex_code.upper()
        return f"https://openmoji.org/php/download_asset.php?type=emoji&emoji_hexcode={hex_code}&emoji_variant={variant}"
    
    def download_icon(self, icon_name, variant='color'):
        """Download a PNG icon from OpenMoji"""
        if icon_name not in self.icon_map:
            print(f"Unknown icon: {icon_name}")
            return False
        
        hex_code = self.icon_map[icon_name]
        url = self.get_openmoji_url(hex_code, variant)
        
        # Create filename - using PNG format
        filename = f"{icon_name}.png"
        filepath = self.icons_dir / filename
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded {filename}")
            return True
            
        except Exception as e:
            print(f"Failed to download {icon_name}: {e}")
            return False
    
    def download_all_icons(self, sizes=[64]):
        """Download all icons as SVG"""
        print(f"Downloading {len(self.icon_map)} OpenMoji icons...")
        
        success_count = 0
        
        for icon_name in self.icon_map.keys():
            if self.download_icon(icon_name):
                success_count += 1
        
        print(f"Successfully downloaded {success_count}/{len(self.icon_map)} icons")
        return success_count == len(self.icon_map)
    
    def get_icon_path(self, icon_name):
        """Get the local path to a PNG icon file"""
        filename = f"{icon_name}.png"
        filepath = self.icons_dir / filename
        
        if filepath.exists():
            return str(filepath)
        
        # Try to download if not found
        print(f"Icon {icon_name} not found, attempting download...")
        if self.download_icon(icon_name):
            return str(filepath)
        
        return None
    
    def list_available_icons(self):
        """List all available icon names"""
        return list(self.icon_map.keys())

if __name__ == '__main__':
    # Download icons when run as script
    manager = OpenMojiIconManager()
    manager.download_all_icons()