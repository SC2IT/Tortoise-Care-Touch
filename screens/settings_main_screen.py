from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import emoji
from screens.base_screen import BaseScreen
from utils.icon_widgets import icon_widget

class SettingsMainScreen(BaseScreen):
    """
    Main settings screen with large buttons for each settings category
    Avoids scrolling by breaking settings into separate screens
    """
    
    def __init__(self, db_manager, **kwargs):
        super().__init__(db_manager=db_manager, **kwargs)
    
    def build_ui(self):
        """Build main settings menu with large category buttons"""
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=self.get_button_spacing())
        
        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=self.get_header_height())
        
        # Create back button with icon
        back_content = icon_widget.create_icon_button_content(
            'back', 'Back', 
            icon_size=(self.get_font_size('medium'), self.get_font_size('medium')),
            spacing=10
        )
        
        back_btn = Button(
            size_hint_x=0.25,
            background_color=(0.4, 0.4, 0.4, 1)
        )
        back_btn.add_widget(back_content)
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)
        
        title = Label(
            text='Settings',
            font_size=self.get_font_size('large'),
            size_hint_x=0.75,
            color=(0.2, 0.6, 0.2, 1)
        )
        header_layout.add_widget(title)
        
        main_layout.add_widget(header_layout)
        
        # Settings category buttons
        settings_grid = GridLayout(
            cols=1,
            spacing=self.get_button_spacing(),
            size_hint_y=0.8
        )
        
        # Category buttons with OpenMoji icons
        categories = [
            {
                'title': "User Management",
                'subtitle': 'Add users, assign tasks, manage profiles',
                'screen': 'settings_users',
                'color': (0.2, 0.6, 0.4, 1),
                'icon': 'users'
            },
            {
                'title': "Tortoise Management", 
                'subtitle': 'Add tortoises, edit profiles, view info',
                'screen': 'settings_tortoises',
                'color': (0.6, 0.4, 0.2, 1),
                'icon': 'tortoise'
            },
            {
                'title': "Connections",
                'subtitle': 'Adafruit.IO, sensors, network settings',
                'screen': 'settings_connections',
                'color': (0.2, 0.4, 0.6, 1),
                'icon': 'wifi'
            },
            {
                'title': "Database",
                'subtitle': 'Backup, restore, import/export data',
                'screen': 'settings_database',
                'color': (0.6, 0.2, 0.6, 1),
                'icon': 'database'
            }
        ]
        
        for category in categories:
            btn_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=self.get_button_height() * 1.5,
                spacing=5
            )
            
            # Create button content with icon and text
            button_content = icon_widget.create_icon_button_content(
                category['icon'], 
                category['title'],
                icon_size=(self.get_font_size('large'), self.get_font_size('large')),
                spacing=15
            )
            
            main_btn = Button(
                background_color=category['color'],
                size_hint_y=0.6
            )
            main_btn.add_widget(button_content)
            main_btn.bind(on_press=lambda x, screen=category['screen']: self.go_to_section(screen))
            
            subtitle = Label(
                text=category['subtitle'],
                font_size=self.get_font_size('small'),
                size_hint_y=0.4,
                color=(0.7, 0.7, 0.7, 1),
                text_size=(None, None)
            )
            
            btn_layout.add_widget(main_btn)
            btn_layout.add_widget(subtitle)
            settings_grid.add_widget(btn_layout)
        
        main_layout.add_widget(settings_grid)
        
        # Quick info section
        info_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        
        # Read version from VERSION file
        version_text = 'Unknown'
        try:
            import os
            version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')
            with open(version_file, 'r') as f:
                version_text = f.read().strip()
        except:
            version_text = 'v0.2.2-alpha'  # Fallback
        
        version_label = Label(
            text=f'Version: {version_text}',
            font_size=self.get_font_size('small'),
            color=(0.5, 0.5, 0.5, 1)
        )
        
        status_label = Label(
            text='Status: Running on Pi Touch Display 2',
            font_size=self.get_font_size('small'),
            color=(0.5, 0.5, 0.5, 1)
        )
        
        info_layout.add_widget(version_label)
        info_layout.add_widget(status_label)
        main_layout.add_widget(info_layout)
        
        self.add_widget(main_layout)
    
    def go_to_section(self, screen_name):
        """Navigate to a specific settings section"""
        # For now, show a placeholder - we'll implement the individual screens next
        if screen_name == 'settings_users':
            # Navigate to user management screen
            self.manager.current = 'settings_users'
        else:
            section_name = screen_name.replace('settings_', '').replace('_', ' ').title()
            self.show_popup('Coming Soon', f'The {section_name} section will be implemented soon!')
    
    def show_popup(self, title, message):
        """Show information popup"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        msg_label = Label(
            text=message,
            text_size=(400, None),
            font_size=self.get_font_size('medium'),
            halign='center'
        )
        content.add_widget(msg_label)
        
        close_btn = Button(
            text='OK',
            size_hint_y=None,
            height=self.get_button_height(),
            font_size=self.get_font_size('medium'),
            background_color=(0.2, 0.6, 0.2, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.7),
            title_size=self.get_font_size('large')
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, instance):
        """Return to home screen"""
        self.manager.current = 'home'