from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from datetime import datetime
from screens.base_screen import BaseScreen

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
            ('Feed Tortoise', 'feeding', (0.2, 0.6, 0.2, 1)),
            ('Health Records', 'health', (0.6, 0.2, 0.2, 1)),
            ('Habitat Monitor', 'habitat', (0.2, 0.2, 0.6, 1)),
            ('Growth Tracking', 'growth', (0.6, 0.6, 0.2, 1)),
            ('Care Reminders', 'reminders', (0.6, 0.4, 0.2, 1)),
            ('Plant Database', 'plants', (0.2, 0.6, 0.6, 1)),
        ]
        
        for text, screen_name, color in buttons:
            btn = Button(
                text=text,
                font_size=self.get_font_size('medium'),
                background_color=color,
                size_hint=(1, 1)
            )
            btn.bind(on_press=lambda x, screen=screen_name: self.go_to_screen(screen))
            nav_grid.add_widget(btn)
        
        main_layout.add_widget(nav_grid)
        
        # Settings button
        settings_btn = Button(
            text='Settings',
            font_size=self.get_font_size('medium'),
            size_hint_y=0.08 if self.is_portrait() else 0.1,
            background_color=(0.4, 0.4, 0.4, 1)
        )
        settings_btn.bind(on_press=lambda x: self.go_to_screen('settings'))
        main_layout.add_widget(settings_btn)
        
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