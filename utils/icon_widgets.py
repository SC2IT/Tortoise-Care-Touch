"""
Kivy Icon Widget Manager for OpenMoji icons
Creates Kivy Image widgets from downloaded PNG icons
"""

import os
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from pathlib import Path

class IconWidget:
    """Creates Kivy widgets for OpenMoji icons"""
    
    def __init__(self):
        self.icons_dir = Path(__file__).parent.parent / 'icons'
    
    def create_icon(self, icon_name, size=(32, 32)):
        """
        Create a Kivy Image widget for an icon
        Returns Image widget if icon exists, otherwise returns None
        """
        icon_path = self.icons_dir / f"{icon_name}.png"
        
        if icon_path.exists():
            return Image(
                source=str(icon_path),
                size_hint=(None, None),
                size=size,
                allow_stretch=True,
                keep_ratio=True
            )
        else:
            print(f"Warning: Icon {icon_name} not found at {icon_path}")
            return None
    
    def create_icon_button_content(self, icon_name, text, icon_size=(24, 24), spacing=5):
        """
        Create a horizontal layout with icon and text for button content
        Returns BoxLayout with icon and label, or just text if icon fails
        """
        content = BoxLayout(orientation='horizontal', spacing=spacing)
        
        # Try to add icon, but don't fail if it doesn't work
        try:
            icon = self.create_icon(icon_name, icon_size)
            if icon:
                icon.size_hint_x = None
                icon.width = icon_size[0]
                content.add_widget(icon)
        except Exception as e:
            print(f"Icon loading failed for {icon_name}: {e}")
        
        # Always add text label as fallback
        label = Label(
            text=text,
            color=(1, 1, 1, 1),
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        content.add_widget(label)
        
        return content
    
    def get_available_icons(self):
        """List all available icon names"""
        if not self.icons_dir.exists():
            return []
        
        icons = []
        for file_path in self.icons_dir.glob('*.png'):
            icons.append(file_path.stem)
        
        return sorted(icons)

# Global instance for easy access
icon_widget = IconWidget()