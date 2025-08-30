#!/usr/bin/env python3
"""
Orientation Test Script
Run this to test orientation detection and UI adaptation
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
from utils.orientation_manager import OrientationManager

# Enable resizing for testing
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '1280')

class OrientationTestApp(App):
    def __init__(self):
        super().__init__()
        self.orientation_manager = OrientationManager()
        
    def build(self):
        self.title = "Orientation Test - Tortoise Care Touch"
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Title
        title = Label(text='Orientation Test', font_size='24sp', size_hint_y=0.1)
        main_layout.add_widget(title)
        
        # Info labels
        self.orientation_label = Label(font_size='18sp', size_hint_y=0.1)
        self.window_size_label = Label(font_size='16sp', size_hint_y=0.1)
        self.layout_info_label = Label(font_size='14sp', size_hint_y=0.2)
        
        main_layout.add_widget(self.orientation_label)
        main_layout.add_widget(self.window_size_label)
        main_layout.add_widget(self.layout_info_label)
        
        # Test buttons grid - adapts to orientation
        self.button_grid = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.4)
        main_layout.add_widget(self.button_grid)
        
        # Control buttons
        controls = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.1)
        
        portrait_btn = Button(text='Test Portrait\n(720x1280)', font_size='14sp')
        portrait_btn.bind(on_press=self.set_portrait)
        controls.add_widget(portrait_btn)
        
        landscape_btn = Button(text='Test Landscape\n(1280x720)', font_size='14sp')
        landscape_btn.bind(on_press=self.set_landscape)
        controls.add_widget(landscape_btn)
        
        refresh_btn = Button(text='Refresh\nInfo', font_size='14sp')
        refresh_btn.bind(on_press=self.update_info)
        controls.add_widget(refresh_btn)
        
        main_layout.add_widget(controls)
        
        # Bind orientation change event
        self.orientation_manager.bind(on_orientation_change=self.on_orientation_change)
        
        # Initial update
        Clock.schedule_once(self.update_info, 0.1)
        Clock.schedule_interval(self.update_info, 1)  # Update every second
        
        return main_layout
    
    def on_orientation_change(self, manager, new_orientation, previous_orientation):
        """Handle orientation changes"""
        print(f"Orientation changed: {previous_orientation} -> {new_orientation}")
        self.update_button_layout()
    
    def update_info(self, *args):
        """Update display information"""
        window_info = self.orientation_manager.get_window_info()
        layout_config = self.orientation_manager.get_layout_config()
        
        self.orientation_label.text = f"Current Orientation: {window_info['orientation'].upper()}"
        self.window_size_label.text = f"Window Size: {window_info['width']} x {window_info['height']}"
        
        layout_info = f"Layout Config:\n"
        layout_info += f"• Navigation Columns: {layout_config['nav_columns']}\n"
        layout_info += f"• Input Columns: {layout_config['input_columns']} x {layout_config['input_rows']}\n"
        layout_info += f"• Button Spacing: {layout_config['button_spacing']}\n"
        layout_info += f"• Font Sizes: L:{layout_config['font_size_large']} M:{layout_config['font_size_medium']} S:{layout_config['font_size_small']}"
        
        self.layout_info_label.text = layout_info
        
        # Update button layout
        self.update_button_layout()
    
    def update_button_layout(self):
        """Update button grid layout based on orientation"""
        self.button_grid.clear_widgets()
        
        layout_config = self.orientation_manager.get_layout_config()
        
        if self.orientation_manager.is_portrait():
            # Portrait: single column
            buttons = ['Button 1', 'Button 2', 'Button 3', 'Button 4', 'Button 5', 'Button 6']
            for btn_text in buttons:
                btn = Button(
                    text=btn_text,
                    font_size=layout_config['font_size_medium'],
                    size_hint_y=None,
                    height=layout_config['button_height']
                )
                self.button_grid.add_widget(btn)
        else:
            # Landscape: two columns
            from kivy.uix.gridlayout import GridLayout
            grid = GridLayout(cols=2, spacing=layout_config['button_spacing'])
            
            buttons = ['Button 1', 'Button 2', 'Button 3', 'Button 4', 'Button 5', 'Button 6']
            for btn_text in buttons:
                btn = Button(
                    text=btn_text,
                    font_size=layout_config['font_size_medium'],
                    size_hint_y=None,
                    height=layout_config['button_height']
                )
                grid.add_widget(btn)
            
            self.button_grid.add_widget(grid)
    
    def set_portrait(self, instance):
        """Force portrait mode for testing"""
        Window.size = (720, 1280)
    
    def set_landscape(self, instance):
        """Force landscape mode for testing"""
        Window.size = (1280, 720)

if __name__ == '__main__':
    OrientationTestApp().run()