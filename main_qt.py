#!/usr/bin/env python3
"""
Tortoise Care Touch - PySide6 Version
Main application entry point for reliable Pi OS compatibility
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Import screens
from qt_screens.home_screen import HomeScreen
from qt_screens.settings_main_screen import SettingsMainScreen
from qt_screens.health_screen import HealthScreen
from qt_screens.health_records_screen import HealthRecordsScreen
from qt_screens.settings_connections_screen import SettingsConnectionsScreen
from qt_screens.habitat_monitor_screen import HabitatMonitorScreen
from qt_screens.growth_tracking_screen import GrowthTrackingScreen
from qt_screens.care_reminders_screen import CareRemindersScreen
from qt_screens.plant_database_screen import PlantDatabaseScreen
from qt_screens.placeholder_screen import PlaceholderScreen
from qt_screens.settings_users_screen import SettingsUsersScreen
from qt_screens.settings_tortoises_screen import SettingsTortoisesScreen
from qt_screens.tortoise_selection_screen import TortoiseSelectionScreen

# Import database
from database.db_manager import DatabaseManager

# Import photo server
from photo_server import run_photo_server_background

class TortoiseCareApp(QMainWindow):
    """Main application window with screen management"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize database
        self.db_manager = DatabaseManager()
        
        # Ensure database is initialized
        try:
            self.db_manager.initialize_database()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")
        
        # Start photo upload server in background
        try:
            self.photo_server_thread = run_photo_server_background()
            print("Photo upload server started successfully")
        except Exception as e:
            print(f"Warning: Could not start photo server: {e}")
        
        # Initialize UI
        self.init_ui()
        self.setup_screens()
        
    def init_ui(self):
        """Initialize main application window"""
        self.setWindowTitle('Tortoise Care Touch - PySide6')
        self.setGeometry(100, 100, 1280, 720)  # 7-inch landscape touch screen resolution
        self.setFixedSize(1280, 720)  # Force exact 7-inch landscape touch display resolution for testing
        
        # Enable touch events
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        
        # Set larger default font for touch interface
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        
        # Create central stacked widget for screen management
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Store screen references
        self.screens = {}
        
    def setup_screens(self):
        """Initialize and add all application screens"""
        # Home screen
        self.screens['home'] = HomeScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['home'])
        
        # Settings main screen
        self.screens['settings_main'] = SettingsMainScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['settings_main'])
        
        # Health screen
        self.screens['health'] = HealthScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['health'])
        
        # Health records screen
        self.screens['health_records'] = HealthRecordsScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['health_records'])
        
        # Settings sub-screens (functional)
        self.screens['settings_users'] = SettingsUsersScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['settings_users'])
        
        self.screens['settings_tortoises'] = SettingsTortoisesScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['settings_tortoises'])
        
        self.screens['settings_connections'] = SettingsConnectionsScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['settings_connections'])
        
        # Tortoise selection screens for different purposes
        self.screens['select_tortoise_feeding'] = TortoiseSelectionScreen(
            self.db_manager, self, return_screen='home', action_name='Feeding'
        )
        self.stacked_widget.addWidget(self.screens['select_tortoise_feeding'])
        
        self.screens['select_tortoise_health'] = TortoiseSelectionScreen(
            self.db_manager, self, return_screen='home', action_name='Health Records'
        )
        self.stacked_widget.addWidget(self.screens['select_tortoise_health'])
        
        self.screens['select_tortoise_care'] = TortoiseSelectionScreen(
            self.db_manager, self, return_screen='home', action_name='Care Entry'
        )
        self.stacked_widget.addWidget(self.screens['select_tortoise_care'])
        
        # Placeholder screens for unimplemented features
        
        # Feeding screen
        self.screens['feeding'] = PlaceholderScreen(
            self.db_manager, self,
            'Feed Tortoise',
            'Complete feeding tracking system with plant safety integration.',
            [
                'Weight-based feeding sessions',
                'Plant safety indicators (green/yellow/red)',
                'Supplement tracking (calcium, vitamins)',
                'Multi-user feeding logs',
                'Behavior notes and observations',
                'Integration with plant database'
            ]
        )
        self.stacked_widget.addWidget(self.screens['feeding'])
        
        # Habitat monitoring screen
        self.screens['habitat'] = HabitatMonitorScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['habitat'])
        
        # Growth tracking screen
        self.screens['growth'] = GrowthTrackingScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['growth'])
        
        # Care reminders screen
        self.screens['reminders'] = CareRemindersScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['reminders'])
        
        # Plant database screen
        self.screens['plants'] = PlantDatabaseScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['plants'])
        
        # About screen
        self.screens['about'] = PlaceholderScreen(
            self.db_manager, self,
            'About',
            'Application information, credits, and technical details.',
            [
                'Version and build information',
                'Source citations and acknowledgments',
                'Technical framework details',
                'Privacy policy and data handling',
                'License information',
                'Contribution guidelines'
            ]
        )
        self.stacked_widget.addWidget(self.screens['about'])
        
        # Set home as default screen
        self.show_screen('home')
        
    def show_screen(self, screen_name):
        """Navigate to a specific screen"""
        if screen_name in self.screens:
            screen = self.screens[screen_name]
            self.stacked_widget.setCurrentWidget(screen)
            
            # Refresh screen if it has an on_enter method
            if hasattr(screen, 'on_enter'):
                screen.on_enter()
        else:
            print(f"Warning: Screen '{screen_name}' not found")
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Close database connection
        if self.db_manager:
            self.db_manager.close()
        event.accept()

def main():
    """Main application entry point"""
    # Create application
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Tortoise Care Touch")
    app.setApplicationVersion("0.3.0-alpha")
    
    # Enable high DPI scaling for touch displays (Qt 6.0+ handles this automatically)
    # app.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # Deprecated in Qt 6+
    
    # Create and show main window
    window = TortoiseCareApp()
    window.show()
    
    # Enable fullscreen for Pi Touch Display
    if len(sys.argv) > 1 and sys.argv[1] == '--fullscreen':
        window.showFullScreen()
    
    # Run application
    sys.exit(app.exec())

if __name__ == '__main__':
    main()