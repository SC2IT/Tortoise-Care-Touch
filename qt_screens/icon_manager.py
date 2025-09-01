"""
Qt Icon Management System
Handles PNG icon loading and integration with PySide6 widgets
"""

import os
from pathlib import Path
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize

class QtIconManager:
    """Manages PNG icons for Qt widgets with fallbacks"""
    
    def __init__(self):
        self.icons_dir = Path(__file__).parent.parent / 'icons'
        self.icon_cache = {}
        
    def get_icon_path(self, icon_name):
        """Get the path to a PNG icon file"""
        icon_path = self.icons_dir / f"{icon_name}.png"
        return icon_path if icon_path.exists() else None
        
    def load_icon(self, icon_name, size=(32, 32)):
        """Load a PNG icon as QIcon with caching"""
        cache_key = f"{icon_name}_{size[0]}_{size[1]}"
        
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
            
        icon_path = self.get_icon_path(icon_name)
        if icon_path and icon_path.exists():
            try:
                pixmap = QPixmap(str(icon_path))
                if not pixmap.isNull():
                    # Scale pixmap to desired size
                    scaled_pixmap = pixmap.scaled(
                        QSize(size[0], size[1]), 
                        aspectRatioMode=1,  # KeepAspectRatio
                        transformMode=1     # SmoothTransformation
                    )
                    icon = QIcon(scaled_pixmap)
                    self.icon_cache[cache_key] = icon
                    return icon
            except Exception as e:
                print(f"Error loading icon {icon_name}: {e}")
                
        return None
        
    def create_icon_button(self, icon_name, text, size=(24, 24), callback=None):
        """Create a QPushButton with PNG icon and text"""
        button = QPushButton(text)
        
        # Try to load and set icon
        icon = self.load_icon(icon_name, size)
        if icon:
            button.setIcon(icon)
            button.setIconSize(QSize(size[0], size[1]))
            
        # Connect callback if provided
        if callback:
            button.clicked.connect(callback)
            
        return button
        
    def get_available_icons(self):
        """Get list of available icon names"""
        if not self.icons_dir.exists():
            return []
            
        icons = []
        for file_path in self.icons_dir.glob('*.png'):
            icons.append(file_path.stem)
            
        return sorted(icons)
        
    def set_button_icon(self, button, icon_name, size=(24, 24)):
        """Set icon on existing QPushButton"""
        icon = self.load_icon(icon_name, size)
        if icon:
            button.setIcon(icon)
            button.setIconSize(QSize(size[0], size[1]))
            return True
        return False

# Global instance for easy access
qt_icon_manager = QtIconManager()


def create_icon_button(icon_name, text, size=(24, 24), callback=None):
    """Convenience function to create icon button"""
    return qt_icon_manager.create_icon_button(icon_name, text, size, callback)


def set_button_icon(button, icon_name, size=(24, 24)):
    """Convenience function to set button icon"""
    return qt_icon_manager.set_button_icon(button, icon_name, size)


def get_available_icons():
    """Convenience function to get available icons"""
    return qt_icon_manager.get_available_icons()