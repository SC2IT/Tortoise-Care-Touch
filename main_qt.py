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

# Import database
from database.db_manager import DatabaseManager

class TortoiseCareApp(QMainWindow):
    """Main application window with screen management"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize database
        self.db_manager = DatabaseManager()
        
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