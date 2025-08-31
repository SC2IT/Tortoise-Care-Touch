"""
Simple icon fallback system - just text with optional emoji
"""

import os
from pathlib import Path

def get_button_text_with_icon(icon_name, text):
    """
    Get button text with optional emoji icon fallback
    If OpenMoji icons aren't working, fall back to simple text
    """
    # Define emoji fallbacks for common icons
    emoji_fallbacks = {
        'back': '← ',
        'settings': '⚙ ',
        'users': '👥 ',
        'tortoise': '🐢 ',
        'wifi': '📶 ',
        'database': '💾 ',
        'medical': '🩺 ',
        'emergency': '⚠ ',
        'phone': '📞 ',
        'apple': '🍎 ',
        'thermometer': '🌡 ',
        'trending-up': '📈 ',
        'bell': '🔔 ',
        'plant': '🌱 ',
        'home': '🏠 ',
        'heart': '❤ ',
    }
    
    # Try to use emoji if available, otherwise just text
    try:
        emoji_prefix = emoji_fallbacks.get(icon_name, '')
        return f"{emoji_prefix}{text}"
    except:
        return text

def has_openmoji_icons():
    """Check if OpenMoji icons are available"""
    icons_dir = Path(__file__).parent.parent / 'icons'
    return icons_dir.exists() and len(list(icons_dir.glob('*.png'))) > 10