from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from datetime import datetime
from screens.base_screen import BaseScreen
from utils.icon_widgets import icon_widget

class HomeScreen(BaseScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(db_manager=db_manager, **kwargs)
        
        # Schedule periodic updates
        Clock.schedule_interval(self.update_display, 30)  # Update every 30 seconds
    
    def build_ui(self):
        """Build UI with orientation awareness"""
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=20, 
            spacing=self.get_button_spacing()
        )
        
        # Header - adjust size based on orientation
        header = Label(
            text='Tortoise Care Touch',
            font_size=self.get_font_size('large'),
            size_hint_y=self.get_header_height(),
            color=(0.2, 0.6, 0.2, 1)
        )
        main_layout.add_widget(header)
        
        # Current time and date
        self.time_label = Label(
            text=datetime.now().strftime('%A, %B %d, %Y - %I:%M %p'),
            font_size=self.get_font_size('medium'),
            size_hint_y=0.08 if self.is_portrait() else 0.12
        )
        main_layout.add_widget(self.time_label)
        
        # Quick status area - adapt layout for orientation
        status_layout = BoxLayout(
            orientation='horizontal' if self.is_landscape() else 'vertical',
            size_hint_y=0.15 if self.is_portrait() else 0.25,
            spacing=10
        )
        
        self.temp_label = Label(text='Temperature: --°C', font_size=self.get_font_size('small'))
        self.humidity_label = Label(text='Humidity: --%', font_size=self.get_font_size('small'))
        self.last_feeding_label = Label(text='Last Feeding: --', font_size=self.get_font_size('small'))
        
        status_layout.add_widget(self.temp_label)
        status_layout.add_widget(self.humidity_label)
        status_layout.add_widget(self.last_feeding_label)
        
        main_layout.add_widget(status_layout)
        
        # Main navigation buttons - adapt columns based on orientation
        nav_grid = GridLayout(
            cols=self.get_nav_columns(),
            spacing=self.get_button_spacing(),
            size_hint_y=0.55 if self.is_portrait() else 0.45
        )
        
        buttons = [
            ('Feed Tortoise', 'feeding', (0.2, 0.6, 0.2, 1), 'apple'),
            ('Health Records', 'health', (0.6, 0.2, 0.2, 1), 'medical'),
            ('Habitat Monitor', 'habitat', (0.2, 0.2, 0.6, 1), 'thermometer'),
            ('Growth Tracking', 'growth', (0.6, 0.6, 0.2, 1), 'trending-up'),
            ('Care Reminders', 'reminders', (0.6, 0.4, 0.2, 1), 'bell'),
            ('Plant Database', 'plants', (0.2, 0.6, 0.6, 1), 'plant'),
        ]
        
        for text, screen_name, color, icon_name in buttons:
            # Create button content with icon and text
            button_content = icon_widget.create_icon_button_content(
                icon_name, 
                text,
                icon_size=(self.get_font_size('large'), self.get_font_size('large')),
                spacing=10
            )
            
            btn = Button(
                background_color=color,
                size_hint=(1, 1)
            )
            btn.add_widget(button_content)
            btn.bind(on_press=lambda x, screen=screen_name: self.go_to_screen(screen))
            nav_grid.add_widget(btn)
        
        main_layout.add_widget(nav_grid)
        
        # Bottom buttons layout
        bottom_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=0.08 if self.is_portrait() else 0.1,
            spacing=10
        )
        
        # About button (small)
        about_btn = Button(
            text='About',
            font_size=self.get_font_size('small'),
            size_hint_x=0.25,
            background_color=(0.3, 0.3, 0.5, 1)
        )
        about_btn.bind(on_press=lambda x: self.go_to_screen('about'))
        bottom_layout.add_widget(about_btn)
        
        # Settings button (main) with icon
        settings_content = icon_widget.create_icon_button_content(
            'settings', 'Settings',
            icon_size=(self.get_font_size('medium'), self.get_font_size('medium')),
            spacing=10
        )
        
        settings_btn = Button(
            size_hint_x=0.75,
            background_color=(0.4, 0.4, 0.4, 1)
        )
        settings_btn.add_widget(settings_content)
        settings_btn.bind(on_press=lambda x: self.go_to_screen('settings_main'))
        bottom_layout.add_widget(settings_btn)
        
        main_layout.add_widget(bottom_layout)
        
        self.add_widget(main_layout)
    
    def handle_orientation_change(self, new_orientation, previous_orientation):
        """Custom handler for orientation changes"""
        # Update time display immediately after orientation change
        self.update_display(0)
    
    def go_to_screen(self, screen_name):
        self.manager.current = screen_name
    
    def update_display(self, dt):
        # Update time
        self.time_label.text = datetime.now().strftime('%A, %B %d, %Y - %I:%M %p')
        
        # Update habitat readings (placeholder for now)
        # TODO: Integrate with Adafruit.IO
        self.temp_label.text = 'Temperature: --°C'
        self.humidity_label.text = 'Humidity: --%'
        
        # Update last feeding info
        # TODO: Get from database
        self.last_feeding_label.text = 'Last Feeding: --'
    
    def on_enter(self):
        # Called when screen becomes active
        self.update_display(0)