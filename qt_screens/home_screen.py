"""
Home screen with main navigation and status display
"""

from datetime import datetime, timedelta
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, 
                              QPushButton, QLabel)
from PySide6.QtCore import Qt, QTimer
from .base_screen import BaseScreen
from .icon_manager import create_icon_button, set_button_icon
from utils.adafruit_io_utils import create_adafruit_connector, get_sensor_thresholds

# Import our sophisticated design system
try:
    from design_system.colors import APP_COLORS
except ImportError:
    # Fallback colors if design system not available
    APP_COLORS = {
        'core': {
            'blue_gray': '#5a7a8a',
            'purple_gray': '#6b5a8a', 
            'teal_gray': '#5a8a7a',
        },
        'blue_gray_family': {
            'lightest': '#e8edf0',
            'base': '#5a7a8a',
            'dark': '#4a6673',
        }
    }

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
        # Touch-optimized spacing for better usability
        self.main_layout.setSpacing(10)  # Consistent 10px spacing
        self.main_layout.setContentsMargins(15, 15, 15, 15)  # Maintain 15px margins
        
        # App title
        title = self.create_title_label('Tortoise Care Touch', 'large')
        self.main_layout.addWidget(title)
        
        # Current time and date
        self.time_label = QLabel()
        time_font = self.time_label.font()
        time_font.setPointSize(14)
        self.time_label.setFont(time_font)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet(f"margin: 5px; color: {APP_COLORS['text']['secondary']};")
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
        
        # Style status labels with design system colors
        for label in [self.temp_label, self.humidity_label, self.last_feeding_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"""
                QLabel {{
                    background-color: {APP_COLORS['backgrounds']['neutral_light']};
                    border: 1px solid {APP_COLORS['core']['blue_gray']};
                    border-radius: 8px;
                    padding: 12px;
                    margin: 5px;
                    font-size: 14px;
                    font-weight: 500;
                    min-height: 20px;
                }}
            """)
            
        status_layout.addWidget(self.temp_label)
        status_layout.addWidget(self.humidity_label)
        status_layout.addWidget(self.last_feeding_label)
        
        self.main_layout.addLayout(status_layout)
        
    def create_navigation_buttons(self):
        """Create main navigation button grid"""
        nav_layout = QGridLayout()
        nav_layout.setSpacing(15)  # Touch-friendly button spacing
        
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
            
            # Apply styling with design system colors - optimized for touch
            if style == 'primary':
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {APP_COLORS['core']['blue_gray']};
                        color: white;
                        border: none;
                        border-radius: 12px;
                        padding: 15px;
                        font-weight: bold;
                        font-size: 18px;
                        text-align: left;
                        padding-left: 25px;
                    }}
                    QPushButton:hover {{
                        background-color: {APP_COLORS['blue_gray_family']['dark']};
                    }}
                    QPushButton:pressed {{
                        background-color: {APP_COLORS['blue_gray_family']['darker']};
                    }}
                """)
            elif style == 'danger':
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {APP_COLORS['core']['teal_gray']};
                        color: white;
                        border: none;
                        border-radius: 12px;
                        padding: 15px;
                        font-weight: bold;
                        font-size: 18px;
                        text-align: left;
                        padding-left: 25px;
                    }}
                    QPushButton:hover {{
                        background-color: {APP_COLORS['teal_gray_family']['dark']};
                    }}
                    QPushButton:pressed {{
                        background-color: {APP_COLORS['teal_gray_family']['darker']};
                    }}
                """)
            elif style == 'secondary':
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {APP_COLORS['analogous']['blue_neighbors'][0]};
                        color: white;
                        border: none;
                        border-radius: 12px;
                        padding: 15px;
                        font-weight: bold;
                        font-size: 18px;
                        text-align: left;
                        padding-left: 25px;
                    }}
                    QPushButton:hover {{
                        background-color: {APP_COLORS['analogous']['blue_neighbors'][1]};
                    }}
                    QPushButton:pressed {{
                        background-color: {APP_COLORS['analogous']['blue_neighbors'][2]};
                    }}
                """)
            elif style == 'warning':
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {APP_COLORS['core']['purple_gray']};
                        color: white;
                        border: none;
                        border-radius: 12px;
                        padding: 15px;
                        font-weight: bold;
                        font-size: 18px;
                        text-align: left;
                        padding-left: 25px;
                    }}
                    QPushButton:hover {{
                        background-color: {APP_COLORS['purple_gray_family']['dark']};
                    }}
                    QPushButton:pressed {{
                        background-color: {APP_COLORS['purple_gray_family']['darker']};
                    }}
                """)
            
            button.setMinimumHeight(90)  # Touch-friendly height
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
        settings_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {APP_COLORS['extended']['nav_secondary']};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 16px;
                text-align: left;
                padding-left: 18px;
            }}
            QPushButton:hover {{
                background-color: {APP_COLORS['purple_gray_family']['dark']};
            }}
            QPushButton:pressed {{
                background-color: {APP_COLORS['purple_gray_family']['darker']};
            }}
        """)
        settings_button.setMinimumWidth(200)
        settings_button.setMinimumHeight(65)  # Touch-friendly height
        bottom_layout.addWidget(settings_button)
        
        # Quit button with icon
        quit_button = create_icon_button('x', 'Quit', (20, 20), self.quit_application)
        quit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {APP_COLORS['extended']['error']};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 16px;
                text-align: left;
                padding-left: 18px;
            }}
            QPushButton:hover {{
                background-color: #c82333;
            }}
            QPushButton:pressed {{
                background-color: #a71e2a;
            }}
        """)
        quit_button.setMinimumWidth(150)
        quit_button.setMinimumHeight(65)  # Touch-friendly height
        bottom_layout.addWidget(quit_button)
        
        self.main_layout.addLayout(bottom_layout)
        
    def update_display(self):
        """Update time and status information"""
        # Update time
        current_time = datetime.now().strftime('%A, %B %d, %Y - %I:%M %p')
        self.time_label.setText(current_time)
        
        # Update habitat readings from Adafruit.IO
        self.update_sensor_data()
        
        # Update last feeding info
        self.update_feeding_info()
    
    def update_sensor_data(self):
        """Update sensor data from Adafruit.IO with stale data warnings"""
        try:
            # Create Adafruit.IO connector
            connector = create_adafruit_connector(self.db_manager)
            
            if not connector:
                # No configuration - show not configured message
                self.temp_label.setText('Temperature: Not Configured')
                self.temp_label.setStyleSheet(self.get_status_style(APP_COLORS['text']['muted']))
                
                self.humidity_label.setText('Humidity: Not Configured')
                self.humidity_label.setStyleSheet(self.get_status_style(APP_COLORS['text']['muted']))
                return
            
            # Get feed names from settings
            temp_feed = self.db_manager.get_setting('temp_feed_name') or 'temperature'
            humidity_feed = self.db_manager.get_setting('humidity_feed_name') or 'humidity'
            
            # Get sensor thresholds
            thresholds = get_sensor_thresholds(self.db_manager)
            
            # Get temperature data
            temp_success, temp_value, temp_msg = connector.get_feed_value(temp_feed)
            if temp_success and temp_value is not None:
                # Check if data is stale (older than 10 minutes)
                is_stale, age_info = self.check_data_staleness(temp_msg)
                temp_status = self.get_threshold_status(temp_value, thresholds['temperature'])
                
                if is_stale:
                    self.temp_label.setText(f'Temperature: {temp_value:.1f}°C ⚠️ STALE')
                    self.temp_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['warning'], warning=True))  # Warning orange for stale
                else:
                    self.temp_label.setText(f'Temperature: {temp_value:.1f}°C')
                    self.temp_label.setStyleSheet(self.get_status_style(temp_status['color']))
            else:
                self.temp_label.setText(f'Temperature: Error')
                self.temp_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['error']))  # Error red
            
            # Get humidity data
            humidity_success, humidity_value, humidity_msg = connector.get_feed_value(humidity_feed)
            if humidity_success and humidity_value is not None:
                # Check if data is stale
                is_stale, age_info = self.check_data_staleness(humidity_msg)
                humidity_status = self.get_threshold_status(humidity_value, thresholds['humidity'])
                
                if is_stale:
                    self.humidity_label.setText(f'Humidity: {humidity_value:.1f}% ⚠️ STALE')
                    self.humidity_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['warning'], warning=True))  # Warning orange for stale
                else:
                    self.humidity_label.setText(f'Humidity: {humidity_value:.1f}%')
                    self.humidity_label.setStyleSheet(self.get_status_style(humidity_status['color']))
            else:
                self.humidity_label.setText(f'Humidity: Error')
                self.humidity_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['error']))  # Error red
                
        except Exception as e:
            # Handle any errors gracefully
            self.temp_label.setText('Temperature: Connection Error')
            self.temp_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['error']))
            
            self.humidity_label.setText('Humidity: Connection Error')
            self.humidity_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['error']))
    
    def check_data_staleness(self, timestamp_msg):
        """Check if data is stale based on timestamp"""
        try:
            # Extract timestamp from message like "Retrieved at 2024-09-02T10:30:00Z"
            if 'Retrieved at' in timestamp_msg:
                timestamp_str = timestamp_msg.split('Retrieved at ')[1]
                # Handle different timestamp formats
                if timestamp_str.endswith('Z'):
                    data_time = datetime.fromisoformat(timestamp_str[:-1])
                else:
                    data_time = datetime.fromisoformat(timestamp_str)
                
                # Calculate age
                now = datetime.now()
                age = now - data_time
                
                # Consider data stale if older than 10 minutes
                is_stale = age > timedelta(minutes=10)
                
                # Format age info
                if age.total_seconds() < 60:
                    age_info = f"{int(age.total_seconds())}s ago"
                elif age.total_seconds() < 3600:
                    age_info = f"{int(age.total_seconds()/60)}m ago"
                else:
                    age_info = f"{int(age.total_seconds()/3600)}h ago"
                
                return is_stale, age_info
        except Exception:
            pass
        
        # Default to stale if we can't parse timestamp
        return True, "unknown age"
    
    def get_threshold_status(self, value, thresholds):
        """Get status based on threshold comparison"""
        if value < thresholds['min']:
            return {'status': 'low', 'color': APP_COLORS['core']['blue_gray']}  # Blue-gray for low
        elif value > thresholds['max']:
            return {'status': 'high', 'color': APP_COLORS['extended']['error']}  # Error red for high
        else:
            return {'status': 'optimal', 'color': APP_COLORS['extended']['success']}  # Success green for optimal
    
    def get_status_style(self, color, warning=False):
        """Get CSS style for status labels using design system colors"""
        if warning:
            return f"""
                QLabel {{
                    background-color: {APP_COLORS['backgrounds']['caution_light']};
                    border: 2px solid {color};
                    border-radius: 8px;
                    padding: 12px;
                    margin: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    color: {APP_COLORS['text']['primary']};
                    min-height: 20px;
                }}
            """
        else:
            # Determine background based on color using design system
            if color == APP_COLORS['extended']['success']:  # Success green
                bg_color = APP_COLORS['backgrounds']['safe_light']
            elif color == APP_COLORS['core']['blue_gray']:  # Blue-gray - low
                bg_color = APP_COLORS['blue_gray_family']['lightest']
            elif color == APP_COLORS['extended']['error']:  # Error red
                bg_color = APP_COLORS['backgrounds']['danger_light']
            else:  # Muted/not configured
                bg_color = APP_COLORS['backgrounds']['neutral_light']
            
            return f"""
                QLabel {{
                    background-color: {bg_color};
                    border: 1px solid {color};
                    border-radius: 8px;
                    padding: 12px;
                    margin: 5px;
                    font-size: 14px;
                    color: {APP_COLORS['text']['primary']};
                    font-weight: bold;
                    min-height: 20px;
                }}
            """
    
    def update_feeding_info(self):
        """Update last feeding information from database"""
        try:
            # Get recent feeding records
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT f.feeding_date, f.notes, t.name as tortoise_name
                FROM feeding_records f
                JOIN tortoises t ON f.tortoise_id = t.id
                ORDER BY f.feeding_date DESC
                LIMIT 1
            """)
            
            result = cursor.fetchone()
            
            if result:
                feeding_date, notes, tortoise_name = result
                # Parse the feeding date
                feed_time = datetime.fromisoformat(feeding_date)
                now = datetime.now()
                time_diff = now - feed_time
                
                # Format time difference
                if time_diff.days > 0:
                    time_str = f"{time_diff.days}d ago"
                elif time_diff.seconds > 3600:
                    time_str = f"{int(time_diff.seconds/3600)}h ago"
                else:
                    time_str = f"{int(time_diff.seconds/60)}m ago"
                
                self.last_feeding_label.setText(f'Last Feeding: {tortoise_name} ({time_str})')
                
                # Color based on time since last feeding
                if time_diff.days > 1:
                    self.last_feeding_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['error']))  # Error red if >1 day
                elif time_diff.days > 0:
                    self.last_feeding_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['warning']))  # Warning orange if >12 hours
                else:
                    self.last_feeding_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['success']))  # Success green if recent
            else:
                self.last_feeding_label.setText('Last Feeding: No records')
                self.last_feeding_label.setStyleSheet(self.get_status_style(APP_COLORS['text']['muted']))
                
        except Exception as e:
            self.last_feeding_label.setText('Last Feeding: Database Error')
            self.last_feeding_label.setStyleSheet(self.get_status_style(APP_COLORS['extended']['error']))
        
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