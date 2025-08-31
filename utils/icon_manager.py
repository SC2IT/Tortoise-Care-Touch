"""
Icon Manager for Tabler Icons integration
Handles loading and displaying SVG icons in Kivy
"""

import os
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label

class IconManager:
    """Manages Tabler icons for the application"""
    
    ICONS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons')
    
    # Icon mapping for our application
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
        'home': 'heart.png',  # Use heart as fallback
        'food': 'heart.png',  # Use heart as fallback
        'plant': 'heart.png',  # Use heart as fallback
        'growth': 'heart.png',  # Use heart as fallback
        'calendar': 'heart.png',  # Use heart as fallback
        'clipboard': 'heart.png',  # Use heart as fallback
        'pill': 'stethoscope.png',  # Use medical icon
        'warning': 'alert-triangle.png',
        'tortoise': 'bug.png',  # Using bug as closest to tortoise
        'back': 'arrow-left.png',
        'info': 'heart.png'  # Use heart as fallback
    }
    
    @classmethod
    def get_icon_path(cls, icon_name):
        """Get the full path to an icon file"""
        if icon_name in cls.ICON_MAP:
            return os.path.join(cls.ICONS_PATH, cls.ICON_MAP[icon_name])
        return None
    
    @classmethod
    def create_icon_widget(cls, icon_name, size=(24, 24), color=(1, 1, 1, 1)):
        """
        Create a Kivy widget with the specified icon
        Uses PNG images if available, falls back to text
        """
        icon_path = cls.get_icon_path(icon_name)
        
        if icon_path and os.path.exists(icon_path):
            # Use PNG image
            return Image(
                source=icon_path,
                size_hint=(None, None),
                size=size,
                allow_stretch=True,
                keep_ratio=True
            )
        else:
            # Fallback to text icons
            fallback_text = {
                'users': '👥',
                'user': '👤',
                'settings': '⚙',
                'database': '💾',
                'wifi': '📶',
                'heart': '❤',
                'medical': '🏥',
                'emergency': '🚨',
                'phone': '📞',
                'home': '🏠',
                'food': '🍎',
                'plant': '🌿',
                'growth': '📈',
                'calendar': '📅',
                'clipboard': '📋',
                'pill': '💊',
                'warning': '⚠',
                'tortoise': '🐢',
                'back': '←',
                'info': 'ℹ'
            }
            
            return Label(
                text=fallback_text.get(icon_name, '•'),
                font_size=f'{size[0]}sp',
                size_hint=(None, None),
                size=size,
                color=color
            )
    
    @classmethod
    def ensure_icons_exist(cls):
        """Ensure all required icons are downloaded"""
        if not os.path.exists(cls.ICONS_PATH):
            os.makedirs(cls.ICONS_PATH)
        
        # For now, we'll use text fallbacks
        # In a real implementation, we'd download the SVG files here
        return True

# Initialize icon manager
IconManager.ensure_icons_exist()