"""
Home screen with main navigation and status display
"""

from datetime import datetime
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, 
                              QPushButton, QLabel)
from PySide6.QtCore import Qt, QTimer
from .base_screen import BaseScreen
from .icon_manager import create_icon_button, set_button_icon

class HomeScreen(BaseScreen):
    """Main home screen with navigation buttons and status display"""
    
    def __init__(self, db_manager, main_window):
        super().__init__(db_manager, main_window)
        
        # Setup timer for regular updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(30000)  # Update every 30 seconds
        
    def build_ui(self):
        """Build home screen UI"""
        # Make layout more compact for better space usage
        self.main_layout.setSpacing(5)  # Reduce from default 10px to 5px
        self.main_layout.setContentsMargins(15, 15, 15, 15)  # Reduce from 20px to 15px
        
        # App title
        title = self.create_title_label('Tortoise Care Touch', 'large')
        self.main_layout.addWidget(title)
        
        # Current time and date
        self.time_label = QLabel()
        time_font = self.time_label.font()
        time_font.setPointSize(14)
        self.time_label.setFont(time_font)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("margin: 5px; color: #424242;")
        self.main_layout.addWidget(self.time_label)
        
        # Status area
        self.create_status_area()
        
        # Main navigation buttons
        self.create_navigation_buttons()
        
        # Add minimal spacing between main and bottom buttons
        self.main_layout.addSpacing(10)
        
        # Bottom buttons
        self.create_bottom_buttons()
        
        # Initial update
        self.update_display()
        
    def create_status_area(self):
        """Create status display area"""
        status_layout = QHBoxLayout()
        
        # Status labels
        self.temp_label = QLabel('Temperature: --°C')
        self.humidity_label = QLabel('Humidity: --%')
        self.last_feeding_label = QLabel('Last Feeding: --')
        
        # Style status labels
        for label in [self.temp_label, self.humidity_label, self.last_feeding_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    background-color: #E8F5E8;
                    border: 1px solid #4CAF50;
                    border-radius: 5px;
                    padding: 8px;
                    margin: 5px;
                    font-size: 12px;
                }
            """)
            
        status_layout.addWidget(self.temp_label)
        status_layout.addWidget(self.humidity_label)
        status_layout.addWidget(self.last_feeding_label)
        
        self.main_layout.addLayout(status_layout)
        
    def create_navigation_buttons(self):
        """Create main navigation button grid"""
        nav_layout = QGridLayout()
        nav_layout.setSpacing(15)
        
        # Navigation buttons with PNG icons and colors
        buttons = [
            ('Feed Tortoise', 'apple', lambda: self.go_to_screen('select_tortoise_feeding'), 'primary'),
            ('Health Records', 'medical', lambda: self.go_to_screen('select_tortoise_health'), 'danger'),
            ('Habitat Monitor', 'thermometer', lambda: self.go_to_screen('habitat'), 'secondary'),
            ('Growth Tracking', 'trending-up', lambda: self.go_to_screen('growth'), 'warning'),
            ('Care Reminders', 'bell', lambda: self.go_to_screen('reminders'), 'warning'),
            ('Plant Database', 'plant', lambda: self.go_to_screen('plants'), 'primary'),
        ]
        
        # Arrange in 2x3 grid
        row, col = 0, 0
        for text, icon_name, callback, style in buttons:
            # Create button with PNG icon
            button = create_icon_button(icon_name, text, (32, 32), callback)
            
            # Apply styling based on class
            if style == 'primary':
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px;
                        font-weight: bold;
                        font-size: 16px;
                        text-align: left;
                        padding-left: 20px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                    QPushButton:pressed {
                        background-color: #3d8b40;
                    }
                """)
            elif style == 'danger':
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px;
                        font-weight: bold;
                        font-size: 16px;
                        text-align: left;
                        padding-left: 20px;
                    }
                    QPushButton:hover {
                        background-color: #d32f2f;
                    }
                    QPushButton:pressed {
                        background-color: #b71c1c;
                    }
                """)
            elif style == 'secondary':
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px;
                        font-weight: bold;
                        font-size: 16px;
                        text-align: left;
                        padding-left: 20px;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                    QPushButton:pressed {
                        background-color: #1565C0;
                    }
                """)
            elif style == 'warning':
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px;
                        font-weight: bold;
                        font-size: 16px;
                        text-align: left;
                        padding-left: 20px;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                    QPushButton:pressed {
                        background-color: #E65100;
                    }
                """)
            
            button.setMinimumHeight(80)
            nav_layout.addWidget(button, row, col)
            
            col += 1
            if col >= 2:
                col = 0
                row += 1
                
        self.main_layout.addLayout(nav_layout)
        
    def create_bottom_buttons(self):
        """Create bottom navigation buttons"""
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)  # Match main navigation button spacing
        
        # About button
        about_button = self.create_button('About', lambda: self.go_to_screen('about'))
        about_button.setMaximumWidth(150)
        bottom_layout.addWidget(about_button)
        
        # Spacer
        bottom_layout.addStretch()
        
        # Settings button with PNG icon
        settings_button = create_icon_button('settings', 'Settings', (24, 24), 
                                           lambda: self.go_to_screen('settings_main'))
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        """)
        settings_button.setMinimumWidth(200)
        settings_button.setMinimumHeight(60)  # Match About button height for touch usability
        bottom_layout.addWidget(settings_button)
        
        # Quit button with icon
        quit_button = create_icon_button('x', 'Quit', (20, 20), self.quit_application)
        quit_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        quit_button.setMinimumWidth(150)
        quit_button.setMinimumHeight(60)  # Match About button height for touch usability
        bottom_layout.addWidget(quit_button)
        
        self.main_layout.addLayout(bottom_layout)
        
    def update_display(self):
        """Update time and status information"""
        # Update time
        current_time = datetime.now().strftime('%A, %B %d, %Y - %I:%M %p')
        self.time_label.setText(current_time)
        
        # Update habitat readings (placeholder for now)
        # TODO: Integrate with Adafruit.IO
        self.temp_label.setText('Temperature: --°C')
        self.humidity_label.setText('Humidity: --%')
        
        # Update last feeding info
        # TODO: Get from database
        self.last_feeding_label.setText('Last Feeding: --')
        
    def on_enter(self):
        """Called when screen becomes active"""
        self.update_display()
    
    def quit_application(self):
        """Quit the application with confirmation"""
        from PySide6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, 'Quit Application', 
            'Are you sure you want to quit Tortoise Care Touch?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.main_window.close()