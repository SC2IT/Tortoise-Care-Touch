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
from qt_screens.placeholder_screen import PlaceholderScreen
from qt_screens.settings_users_screen import SettingsUsersScreen
from qt_screens.settings_tortoises_screen import SettingsTortoisesScreen

# Import database
from database.db_manager import DatabaseManager

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
        
        # Initialize UI
        self.init_ui()
        self.setup_screens()
        
    def init_ui(self):
        """Initialize main application window"""
        self.setWindowTitle('Tortoise Care Touch - PySide6')
        self.setGeometry(100, 100, 800, 480)  # Pi Touch Display 2 resolution
        
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
        
        # Settings sub-screens (functional)
        self.screens['settings_users'] = SettingsUsersScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['settings_users'])
        
        self.screens['settings_tortoises'] = SettingsTortoisesScreen(self.db_manager, self)
        self.stacked_widget.addWidget(self.screens['settings_tortoises'])
        
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
        self.screens['habitat'] = PlaceholderScreen(
            self.db_manager, self,
            'Habitat Monitor',
            'Real-time temperature and humidity monitoring via Adafruit.IO.',
            [
                'Live temperature and humidity readings',
                'Adafruit.IO sensor integration',
                'Alert system for out-of-range conditions',
                'Historical data logging and charts',
                'Multiple sensor support',
                'Automated data collection'
            ]
        )
        self.stacked_widget.addWidget(self.screens['habitat'])
        
        # Growth tracking screen
        self.screens['growth'] = PlaceholderScreen(
            self.db_manager, self,
            'Growth Tracking',
            'Photo documentation and measurement tracking system.',
            [
                'Photo import from mobile devices',
                'Weight and size measurements',
                'Growth charts and visualizations',
                'Progress comparison over time',
                'Photo gallery with timestamps',
                'Measurement history tracking'
            ]
        )
        self.stacked_widget.addWidget(self.screens['growth'])
        
        # Care reminders screen
        self.screens['reminders'] = PlaceholderScreen(
            self.db_manager, self,
            'Care Reminders',
            'Task scheduling and notification system for daily tortoise care.',
            [
                'Daily, weekly, monthly care routines',
                'Task completion tracking',
                'Multi-user task assignments',
                'Notification system',
                'Care schedule customization',
                'Task history and compliance'
            ]
        )
        self.stacked_widget.addWidget(self.screens['reminders'])
        
        # Plant database screen
        self.screens['plants'] = PlaceholderScreen(
            self.db_manager, self,
            'Plant Database',
            'Comprehensive plant safety database with 60+ plants for tortoise feeding.',
            [
                'Complete plant safety classifications',
                'Plant photos (leaves, flowers, full plant)',
                'Visual plant identification guide',
                'Scientific names and nutrition info',
                'Feeding frequency recommendations',
                'Toxic plant warnings and alternatives',
                'Search and filter functionality'
            ]
        )
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
    app.setApplicationVersion("0.3.0-qt")
    
    # Enable high DPI scaling for touch displays
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    
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