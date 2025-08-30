#!/usr/bin/env python3
"""
Tortoise Care Touch
Main entry point for the touch-screen tortoise care management system
Designed for Raspberry Pi 4 with Pi Touch Display 2
"""

import os
import sys
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
        self.db_manager = DatabaseManager()
        self.orientation_manager = OrientationManager()
        
    def build(self):
        self.title = "Tortoise Care Touch"
        
        # Initialize database
        self.db_manager.initialize_database()
        
        # Create screen manager
        sm = ScreenManager()
        
        # Create all screens
        screens = [
            HomeScreen(name='home', db_manager=self.db_manager),
            FeedingScreen(name='feeding', db_manager=self.db_manager),
            HealthScreen(name='health', db_manager=self.db_manager),
            HabitatScreen(name='habitat', db_manager=self.db_manager),
            GrowthScreen(name='growth', db_manager=self.db_manager),
            RemindersScreen(name='reminders', db_manager=self.db_manager),
            PlantsScreen(name='plants', db_manager=self.db_manager),
            SettingsMainScreen(name='settings', db_manager=self.db_manager),
            SettingsScreen(name='settings_users', db_manager=self.db_manager)
        ]
        
        # Set orientation manager for each screen and add to screen manager
        for screen in screens:
            if hasattr(screen, 'set_orientation_manager'):
                screen.set_orientation_manager(self.orientation_manager)
            sm.add_widget(screen)
        
        # Log initial orientation info
        Logger.info(f"App started with orientation: {self.orientation_manager.current_orientation}")
        Logger.info(f"Window info: {self.orientation_manager.get_window_info()}")
        
        return sm

    def on_stop(self):
        # Clean up database connection
        if hasattr(self, 'db_manager'):
            self.db_manager.close()

if __name__ == '__main__':
    TortoiseCareApp().run()