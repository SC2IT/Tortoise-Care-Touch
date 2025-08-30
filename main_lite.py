#!/usr/bin/env python3
"""
Tortoise Care Touch - Lite Version
Performance-optimized version for slower systems
"""

import os
import sys
import logging
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.logger import Logger
from kivy.clock import Clock

# Configure Kivy for better performance
Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'fullscreen', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', '1')
Config.set('kivy', 'exit_on_escape', '1')
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '1280')

# Performance optimizations
Config.set('graphics', 'vsync', '0')  # Disable vsync for better performance
Config.set('graphics', 'maxfps', '30')  # Limit FPS to save resources

class LoadingScreen(BoxLayout):
    """Simple loading screen while app initializes"""
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.padding = 50
        self.spacing = 20
        
        # Loading message
        self.loading_label = Label(
            text='Loading Tortoise Care Touch...',
            font_size='24sp',
            size_hint_y=0.2
        )
        self.add_widget(self.loading_label)
        
        # Progress indicator
        self.progress_label = Label(
            text='Initializing...',
            font_size='16sp',
            size_hint_y=0.1,
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(self.progress_label)
    
    def update_progress(self, message):
        """Update loading progress"""
        self.progress_label.text = message
        Logger.info(f"Tortoise Care Touch Lite: {message}")

class TortoiseCareAppLite(App):
    def __init__(self):
        super().__init__()
        self.loading_screen = None
        self.db_manager = None
        self.screens_loaded = False
        
    def build(self):
        Logger.info("Tortoise Care Touch Lite: Starting optimized version...")
        self.title = "Tortoise Care Touch (Performance Mode)"
        
        # Create loading screen first
        self.loading_screen = LoadingScreen()
        
        # Schedule delayed initialization to show loading screen
        Clock.schedule_once(self.initialize_app, 0.1)
        
        return self.loading_screen
    
    def initialize_app(self, dt):
        """Initialize app components in background"""
        try:
            # Update progress
            self.loading_screen.update_progress("Loading database...")
            
            # Initialize database with minimal delay
            from database.db_manager import DatabaseManager
            self.db_manager = DatabaseManager()
            self.db_manager.initialize_database()
            
            # Schedule screen loading
            Clock.schedule_once(self.load_essential_screens, 0.1)
            
        except Exception as e:
            Logger.error(f"Tortoise Care Touch Lite: Initialization error: {e}")
            self.loading_screen.update_progress(f"Error: {e}")
            self.stop()
    
    def load_essential_screens(self, dt):
        """Load only essential screens first"""
        try:
            self.loading_screen.update_progress("Loading screens...")
            
            # Import screens with minimal performance impact
            from screens.base_screen import BaseScreen
            from screens.home_screen import HomeScreen
            from screens.feeding_screen import FeedingScreen
            
            # Create screen manager
            sm = ScreenManager()
            
            # Add essential screens only
            essential_screens = [
                ('home', HomeScreen),
                ('feeding', FeedingScreen),
            ]
            
            for screen_name, screen_class in essential_screens:
                try:
                    screen = screen_class(name=screen_name, db_manager=self.db_manager)
                    sm.add_widget(screen)
                    Logger.info(f"Tortoise Care Touch Lite: ✓ {screen_name} loaded")
                except Exception as e:
                    Logger.error(f"Tortoise Care Touch Lite: ✗ Error loading {screen_name}: {e}")
            
            # Switch to main app
            self.root_window.remove_widget(self.loading_screen)
            self.root_window.add_widget(sm)
            
            # Schedule loading of remaining screens in background
            Clock.schedule_once(self.load_remaining_screens, 1.0)
            
            Logger.info("Tortoise Care Touch Lite: Essential screens loaded, app ready!")
            
        except Exception as e:
            Logger.error(f"Tortoise Care Touch Lite: Screen loading error: {e}")
            self.loading_screen.update_progress(f"Screen loading error: {e}")
    
    def load_remaining_screens(self, dt):
        """Load remaining screens in background"""
        try:
            Logger.info("Tortoise Care Touch Lite: Loading additional screens...")
            
            # Get current screen manager
            sm = self.root_window.children[0]
            
            # Import and add remaining screens
            remaining_screens = [
                ('health', 'screens.health_screen', 'HealthScreen'),
                ('plants', 'screens.plants_screen', 'PlantsScreen'),
                ('settings_main', 'screens.settings_main_screen', 'SettingsMainScreen'),
            ]
            
            for screen_name, module_name, class_name in remaining_screens:
                try:
                    # Dynamic import to reduce initial load time
                    module = __import__(module_name, fromlist=[class_name])
                    screen_class = getattr(module, class_name)
                    
                    screen = screen_class(name=screen_name, db_manager=self.db_manager)
                    sm.add_widget(screen)
                    Logger.info(f"Tortoise Care Touch Lite: ✓ {screen_name} added")
                    
                    # Small delay between screens to prevent blocking
                    Clock.schedule_once(lambda dt: None, 0.1)
                    
                except Exception as e:
                    Logger.error(f"Tortoise Care Touch Lite: ✗ Error loading {screen_name}: {e}")
            
            self.screens_loaded = True
            Logger.info("Tortoise Care Touch Lite: All screens loaded successfully!")
            
        except Exception as e:
            Logger.error(f"Tortoise Care Touch Lite: Background loading error: {e}")
    
    def on_stop(self):
        # Clean up database connection
        if hasattr(self, 'db_manager') and self.db_manager:
            self.db_manager.close()
        Logger.info("Tortoise Care Touch Lite: Application stopped")

if __name__ == '__main__':
    # Set environment variables for better performance
    os.environ['KIVY_WINDOW'] = 'sdl2'  # Use SDL2 for better performance
    os.environ['KIVY_GL_BACKEND'] = 'gl'  # Use OpenGL
    
    Logger.info("Starting Tortoise Care Touch in Performance Mode...")
    TortoiseCareAppLite().run()