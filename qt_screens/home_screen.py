"""
Home screen with main navigation and status display
"""

from datetime import datetime
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, 
                              QPushButton, QLabel)
from PySide6.QtCore import Qt, QTimer
from .base_screen import BaseScreen

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
        # App title
        title = self.create_title_label('Tortoise Care Touch', 'large')
        self.main_layout.addWidget(title)
        
        # Current time and date
        self.time_label = QLabel()
        time_font = self.time_label.font()
        time_font.setPointSize(14)
        self.time_label.setFont(time_font)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("margin: 10px; color: #424242;")
        self.main_layout.addWidget(self.time_label)
        
        # Status area
        self.create_status_area()
        
        # Main navigation buttons
        self.create_navigation_buttons()
        
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
        
        # Navigation buttons with icons and colors
        buttons = [
            ('🍎 Feed Tortoise', lambda: self.go_to_screen('feeding'), 'primary'),
            ('🩺 Health Records', lambda: self.go_to_screen('health'), 'danger'),
            ('🌡️ Habitat Monitor', lambda: self.go_to_screen('habitat'), 'secondary'),
            ('📈 Growth Tracking', lambda: self.go_to_screen('growth'), 'warning'),
            ('🔔 Care Reminders', lambda: self.go_to_screen('reminders'), 'warning'),
            ('🌱 Plant Database', lambda: self.go_to_screen('plants'), 'primary'),
        ]
        
        # Arrange in 2x3 grid
        row, col = 0, 0
        for text, callback, style in buttons:
            button = self.create_button(text, callback, style)
            button.setMinimumHeight(80)
            
            # Make button text larger
            font = button.font()
            font.setPointSize(16)
            button.setFont(font)
            
            nav_layout.addWidget(button, row, col)
            
            col += 1
            if col >= 2:
                col = 0
                row += 1
                
        self.main_layout.addLayout(nav_layout)
        
    def create_bottom_buttons(self):
        """Create bottom navigation buttons"""
        bottom_layout = QHBoxLayout()
        
        # About button
        about_button = self.create_button('About', lambda: self.go_to_screen('about'))
        about_button.setMaximumWidth(150)
        bottom_layout.addWidget(about_button)
        
        # Spacer
        bottom_layout.addStretch()
        
        # Settings button
        settings_button = self.create_button('⚙️ Settings', 
                                           lambda: self.go_to_screen('settings_main'), 
                                           'default')
        settings_button.setMinimumWidth(200)
        bottom_layout.addWidget(settings_button)
        
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