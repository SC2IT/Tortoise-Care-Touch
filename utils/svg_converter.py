"""
Simple SVG to display converter for Kivy
Creates displayable content from SVG icons
"""

import os
import re
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

class SVGIcon(BoxLayout):
    """Simple SVG icon display widget for Kivy"""
    
    def __init__(self, icon_name, size=(32, 32), color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (None, None)
        self.size = size
        
        # For now, create a colored square as icon placeholder
        # In production, this would render the actual SVG
        icon_label = Label(
            text='■',
            font_size=f'{size[0]}sp',
            size_hint=(None, None),
            size=size,
            color=color,
            halign='center',
            valign='middle'
        )
        
        self.add_widget(icon_label)

class IconButton(BoxLayout):
    """Button with icon and text"""
    
    def __init__(self, icon_name, text, icon_size=(24, 24), **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        
        # Add icon
        icon = SVGIcon(icon_name, size=icon_size)
        self.add_widget(icon)
        
        # Add text label
        text_label = Label(
            text=text,
            size_hint_x=None,
            width=200,
            text_size=(200, None),
            halign='left',
            valign='middle'
        )
        self.add_widget(text_label)