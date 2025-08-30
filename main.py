#!/usr/bin/env python3
"""
Tortoise Care Touch
Main entry point for the touch-screen tortoise care management system
Designed for Raspberry Pi 4 with Pi Touch Display 2
"""

import os
import sys
import logging
import traceback
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.logger import Logger
from database.db_manager import DatabaseManager
from utils.orientation_manager import OrientationManager
from screens.home_screen import HomeScreen
from screens.feeding_screen import FeedingScreen
from screens.health_screen import HealthScreen
from screens.habitat_screen import HabitatScreen
from screens.growth_screen import GrowthScreen
from screens.reminders_screen import RemindersScreen
from screens.plants_screen import PlantsScreen
from screens.settings_screen import SettingsScreen
from screens.settings_main_screen import SettingsMainScreen
from screens.settings_users_screen import SettingsUsersScreen
from screens.settings_tortoises_screen import SettingsTortoisesScreen
from screens.settings_connections_screen import SettingsConnectionsScreen
from screens.settings_database_screen import SettingsDatabaseScreen
from screens.about_screen import AboutScreen

# Configure Kivy for Pi Touch Display 2 with dynamic orientation
Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'fullscreen', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', '1')  # Enable resizing for orientation changes
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.set('kivy', 'exit_on_escape', '1')
Config.set('graphics', 'width', '720')    # Default to portrait
Config.set('graphics', 'height', '1280')

class TortoiseCareApp(App):
    def __init__(self):
        super().__init__()
        try:
            Logger.info("Tortoise Care Touch: Initializing application...")
            self.db_manager = DatabaseManager()
            Logger.info("Tortoise Care Touch: DatabaseManager created")
            self.orientation_manager = OrientationManager()
            Logger.info("Tortoise Care Touch: OrientationManager created")
        except Exception as e:
            Logger.error(f"Tortoise Care Touch: Initialization error: {e}")
            traceback.print_exc()
            raise
        
    def build(self):
        try:
            Logger.info("Tortoise Care Touch: Building UI...")
            self.title = "Tortoise Care Touch"
            
            # Initialize database
            Logger.info("Tortoise Care Touch: Initializing database...")
            self.db_manager.initialize_database()
            Logger.info("Tortoise Care Touch: Database initialized successfully")
            
            # Create screen manager
            Logger.info("Tortoise Care Touch: Creating screen manager...")
            sm = ScreenManager()
            
            # Create all screens with error handling
            Logger.info("Tortoise Care Touch: Creating screens...")
            screen_configs = [
                ('home', HomeScreen),
                ('feeding', FeedingScreen),
                ('health', HealthScreen),
                ('habitat', HabitatScreen),
                ('growth', GrowthScreen),
                ('reminders', RemindersScreen),
                ('plants', PlantsScreen),
                ('settings_main', SettingsMainScreen),
                ('settings', SettingsScreen),
                ('settings_users', SettingsUsersScreen),
                ('settings_tortoises', SettingsTortoisesScreen),
                ('settings_connections', SettingsConnectionsScreen),
                ('settings_database', SettingsDatabaseScreen),
                ('about', AboutScreen)
            ]
            
            screens = []
            for screen_name, screen_class in screen_configs:
                try:
                    Logger.info(f"Tortoise Care Touch: Creating {screen_name} screen...")
                    screen = screen_class(name=screen_name, db_manager=self.db_manager)
                    screens.append(screen)
                    Logger.info(f"Tortoise Care Touch: ✓ {screen_name} screen created")
                except Exception as e:
                    Logger.error(f"Tortoise Care Touch: ✗ Error creating {screen_name} screen: {e}")
                    traceback.print_exc()
                    raise
            
            # Set orientation manager for each screen and add to screen manager
            Logger.info("Tortoise Care Touch: Setting up screens...")
            for screen in screens:
                try:
                    if hasattr(screen, 'set_orientation_manager'):
                        screen.set_orientation_manager(self.orientation_manager)
                    sm.add_widget(screen)
                    Logger.info(f"Tortoise Care Touch: ✓ {screen.name} screen added to manager")
                except Exception as e:
                    Logger.error(f"Tortoise Care Touch: ✗ Error setting up {screen.name} screen: {e}")
                    traceback.print_exc()
                    raise
            
            # Log initial orientation info
            Logger.info(f"Tortoise Care Touch: App started with orientation: {self.orientation_manager.current_orientation}")
            Logger.info(f"Tortoise Care Touch: Window info: {self.orientation_manager.get_window_info()}")
            Logger.info("Tortoise Care Touch: UI build completed successfully!")
            
            return sm
        
        except Exception as e:
            Logger.error(f"Tortoise Care Touch: Build error: {e}")
            traceback.print_exc()
            raise

    def on_stop(self):
        # Clean up database connection
        if hasattr(self, 'db_manager'):
            self.db_manager.close()

if __name__ == '__main__':
    TortoiseCareApp().run()