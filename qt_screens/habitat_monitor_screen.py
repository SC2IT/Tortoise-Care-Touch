"""
Habitat Monitor Screen - Real-time temperature and humidity monitoring via Adafruit.IO
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QScrollArea, QWidget, QMessageBox,
                              QProgressBar, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from .base_screen import BaseScreen
from .icon_manager import create_icon_button
import datetime

class HabitatMonitorScreen(BaseScreen):
    """Real-time Habitat Monitoring Screen"""
    
    def build_ui(self):
        """Build habitat monitoring UI"""
        # Header
        header = self.create_header('🌡️ Habitat Monitor', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Status and refresh section
        self.create_status_section()
        
        # Current readings section
        self.create_current_readings_section()
        
        # Alert thresholds section
        self.create_thresholds_section()
        
        # Recent alerts section
        self.create_alerts_section()
        
        # Setup auto-refresh timer
        self.setup_refresh_timer()
        
        # Initial data load
        self.refresh_data()
    
    def create_status_section(self):
        """Create connection status and refresh controls"""
        status_widget = QWidget()
        status_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                margin: 5px 0;
            }
        """)
        
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(15, 15, 15, 15)
        
        # Connection status
        self.connection_status_label = QLabel('⏳ Checking connection...')
        self.connection_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #666;
            }
        """)
        status_layout.addWidget(self.connection_status_label)
        
        status_layout.addStretch()
        
        # Last update time
        self.last_update_label = QLabel('Last update: Never')
        self.last_update_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #777;
                font-style: italic;
            }
        """)
        status_layout.addWidget(self.last_update_label)
        
        # Auto-refresh toggle
        self.auto_refresh_btn = QPushButton('Auto-Refresh: ON')
        self.auto_refresh_btn.setCheckable(True)
        self.auto_refresh_btn.setChecked(True)
        self.auto_refresh_btn.clicked.connect(self.toggle_auto_refresh)
        self.auto_refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:checked { background-color: #4CAF50; }
            QPushButton:!checked { background-color: #757575; }
        """)
        status_layout.addWidget(self.auto_refresh_btn)
        
        # Manual refresh button
        refresh_btn = create_icon_button('activity', 'Refresh', (16, 16), self.refresh_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        status_layout.addWidget(refresh_btn)
        
        self.main_layout.addWidget(status_widget)
    
    def create_current_readings_section(self):
        """Create current sensor readings display"""
        # Section title
        section_title = QLabel('📊 Current Readings')
        section_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2196F3;
                margin: 15px 5px 10px 5px;
            }
        """)
        self.main_layout.addWidget(section_title)
        
        # Readings grid
        readings_widget = QWidget()
        readings_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                margin: 5px 0;
            }
        """)
        
        readings_layout = QGridLayout(readings_widget)
        readings_layout.setContentsMargins(20, 20, 20, 20)
        readings_layout.setSpacing(20)
        
        # Temperature reading
        self.create_reading_widget(readings_layout, 0, 0, '🌡️', 'Temperature', 'temp')
        
        # Humidity reading  
        self.create_reading_widget(readings_layout, 0, 1, '💧', 'Humidity', 'humidity')
        
        self.main_layout.addWidget(readings_widget)
    
    def create_reading_widget(self, parent_layout, row, col, icon, title, reading_type):
        """Create a single reading widget"""
        # Container
        reading_frame = QFrame()
        reading_frame.setFrameStyle(QFrame.Box)
        reading_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                background-color: #f9f9f9;
            }
        """)
        
        reading_layout = QVBoxLayout(reading_frame)
        reading_layout.setAlignment(Qt.AlignCenter)
        
        # Icon and title
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        reading_layout.addLayout(header_layout)
        
        # Current value
        value_label = QLabel('--')
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #2196F3;
                margin: 10px 0;
            }
        """)
        reading_layout.addWidget(value_label)
        
        # Store reference for updates
        if reading_type == 'temp':
            self.temp_value_label = value_label
        elif reading_type == 'humidity':
            self.humidity_value_label = value_label
        
        # Status indicator
        status_label = QLabel('No data')
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #777;
                padding: 4px 8px;
                border-radius: 12px;
                background-color: #e0e0e0;
            }
        """)
        reading_layout.addWidget(status_label)
        
        # Store reference for updates
        if reading_type == 'temp':
            self.temp_status_label = status_label
        elif reading_type == 'humidity':
            self.humidity_status_label = status_label
        
        parent_layout.addWidget(reading_frame, row, col)
    
    def create_thresholds_section(self):
        """Create alert thresholds display"""
        # Section title
        section_title = QLabel('⚠️ Alert Thresholds')
        section_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FF9800;
                margin: 15px 5px 10px 5px;
            }
        """)
        self.main_layout.addWidget(section_title)
        
        # Thresholds info
        thresholds_widget = QWidget()
        thresholds_widget.setStyleSheet("""
            QWidget {
                background-color: #fff8e1;
                border: 2px solid #ffcc02;
                border-radius: 8px;
                padding: 5px;
                margin: 5px 0;
            }
        """)
        
        thresholds_layout = QVBoxLayout(thresholds_widget)
        thresholds_layout.setContentsMargins(15, 15, 15, 15)
        
        self.thresholds_label = QLabel('Loading threshold settings...')
        self.thresholds_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333;
            }
        """)
        thresholds_layout.addWidget(self.thresholds_label)
        
        # Configure button
        config_btn = QPushButton('Configure Alerts')
        config_btn.clicked.connect(self.configure_alerts)
        config_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover { background-color: #F57C00; }
        """)
        thresholds_layout.addWidget(config_btn)
        
        self.main_layout.addWidget(thresholds_widget)
    
    def create_alerts_section(self):
        """Create recent alerts section"""
        # Section title
        section_title = QLabel('🚨 Recent Alerts')
        section_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #f44336;
                margin: 15px 5px 10px 5px;
            }
        """)
        self.main_layout.addWidget(section_title)
        
        # Alerts container
        alerts_widget = QWidget()
        alerts_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                margin: 5px 0;
            }
        """)
        
        alerts_layout = QVBoxLayout(alerts_widget)
        alerts_layout.setContentsMargins(15, 15, 15, 15)
        
        self.alerts_label = QLabel('No recent alerts')
        self.alerts_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #4CAF50;
                font-weight: bold;
            }
        """)
        alerts_layout.addWidget(self.alerts_label)
        
        self.main_layout.addWidget(alerts_widget)
    
    def setup_refresh_timer(self):
        """Setup automatic refresh timer"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
    
    def toggle_auto_refresh(self):
        """Toggle automatic refresh"""
        if self.auto_refresh_btn.isChecked():
            self.refresh_timer.start(30000)
            self.auto_refresh_btn.setText('Auto-Refresh: ON')
        else:
            self.refresh_timer.stop()
            self.auto_refresh_btn.setText('Auto-Refresh: OFF')
    
    def refresh_data(self):
        """Refresh sensor data from Adafruit.IO"""
        try:
            # Update connection status
            self.connection_status_label.setText('🔄 Refreshing...')
            self.connection_status_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: bold;
                    color: #2196F3;
                }
            """)
            
            # Get Adafruit.IO settings
            username = self.db_manager.get_setting('adafruit_io_username')
            api_key = self.db_manager.get_setting('adafruit_io_key')
            temp_feed = self.db_manager.get_setting('temp_feed_name') or 'temperature'
            humidity_feed = self.db_manager.get_setting('humidity_feed_name') or 'humidity'
            
            if not username or not api_key:
                self.show_configuration_needed()
                return
            
            # Try to fetch data from Adafruit.IO
            try:
                from Adafruit_IO import Client
                aio = Client(username, api_key)
                
                # Get temperature data
                try:
                    temp_data = aio.receive(temp_feed)
                    temp_value = float(temp_data.value)
                    self.update_temperature_display(temp_value)
                except Exception as e:
                    self.temp_value_label.setText('Error')
                    self.temp_status_label.setText('Feed not found')
                    self.temp_status_label.setStyleSheet("""
                        QLabel {
                            font-size: 12px;
                            color: white;
                            padding: 4px 8px;
                            border-radius: 12px;
                            background-color: #f44336;
                        }
                    """)
                
                # Get humidity data
                try:
                    humidity_data = aio.receive(humidity_feed)
                    humidity_value = float(humidity_data.value)
                    self.update_humidity_display(humidity_value)
                except Exception as e:
                    self.humidity_value_label.setText('Error')
                    self.humidity_status_label.setText('Feed not found')
                    self.humidity_status_label.setStyleSheet("""
                        QLabel {
                            font-size: 12px;
                            color: white;
                            padding: 4px 8px;
                            border-radius: 12px;
                            background-color: #f44336;
                        }
                    """)
                
                # Update connection status
                self.connection_status_label.setText('✅ Connected to Adafruit.IO')
                self.connection_status_label.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        font-weight: bold;
                        color: #4CAF50;
                    }
                """)
                
                # Update last refresh time
                now = datetime.datetime.now()
                self.last_update_label.setText(f'Last update: {now.strftime("%H:%M:%S")}')
                
            except ImportError:
                self.show_library_missing()
            except Exception as e:
                self.show_connection_error(str(e))
                
        except Exception as e:
            self.show_general_error(str(e))
        
        # Update thresholds display
        self.update_thresholds_display()
    
    def update_temperature_display(self, temp_value):
        """Update temperature display"""
        self.temp_value_label.setText(f'{temp_value:.1f}°C')
        
        # Get thresholds
        temp_min = float(self.db_manager.get_setting('temp_min') or 20)
        temp_max = float(self.db_manager.get_setting('temp_max') or 35)
        
        # Determine status
        if temp_value < temp_min:
            status_text = 'Too Cold'
            status_color = '#2196F3'
        elif temp_value > temp_max:
            status_text = 'Too Hot'
            status_color = '#f44336'
        else:
            status_text = 'Optimal'
            status_color = '#4CAF50'
        
        self.temp_status_label.setText(status_text)
        self.temp_status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                background-color: {status_color};
                font-weight: bold;
            }}
        """)
    
    def update_humidity_display(self, humidity_value):
        """Update humidity display"""
        self.humidity_value_label.setText(f'{humidity_value:.1f}%')
        
        # Get thresholds
        humidity_min = float(self.db_manager.get_setting('humidity_min') or 60)
        humidity_max = float(self.db_manager.get_setting('humidity_max') or 80)
        
        # Determine status
        if humidity_value < humidity_min:
            status_text = 'Too Dry'
            status_color = '#FF9800'
        elif humidity_value > humidity_max:
            status_text = 'Too Humid'
            status_color = '#2196F3'
        else:
            status_text = 'Optimal'
            status_color = '#4CAF50'
        
        self.humidity_status_label.setText(status_text)
        self.humidity_status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                background-color: {status_color};
                font-weight: bold;
            }}
        """)
    
    def update_thresholds_display(self):
        """Update thresholds information"""
        temp_min = self.db_manager.get_setting('temp_min') or '20'
        temp_max = self.db_manager.get_setting('temp_max') or '35'
        humidity_min = self.db_manager.get_setting('humidity_min') or '60'
        humidity_max = self.db_manager.get_setting('humidity_max') or '80'
        
        thresholds_text = (f'Temperature: {temp_min}°C - {temp_max}°C\n'
                          f'Humidity: {humidity_min}% - {humidity_max}%')
        
        self.thresholds_label.setText(thresholds_text)
    
    def show_configuration_needed(self):
        """Show configuration needed message"""
        self.connection_status_label.setText('⚠️ Configuration needed')
        self.connection_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #FF9800;
            }
        """)
        
        self.temp_value_label.setText('--')
        self.humidity_value_label.setText('--')
        
        self.temp_status_label.setText('Not configured')
        self.humidity_status_label.setText('Not configured')
        
        for label in [self.temp_status_label, self.humidity_status_label]:
            label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 12px;
                    background-color: #757575;
                }
            """)
    
    def show_library_missing(self):
        """Show library missing message"""
        self.connection_status_label.setText('❌ Library missing')
        self.connection_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #f44336;
            }
        """)
        
        QMessageBox.warning(self, 'Missing Library', 
                          'Adafruit.IO library not installed.\n\n'
                          'Install with: pip install adafruit-circuitpython-io')
    
    def show_connection_error(self, error_msg):
        """Show connection error"""
        self.connection_status_label.setText('❌ Connection failed')
        self.connection_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #f44336;
            }
        """)
        
        if 'Unauthorized' in error_msg or '401' in error_msg:
            self.alerts_label.setText('⚠️ Invalid Adafruit.IO credentials')
        elif 'Network' in error_msg or 'Connection' in error_msg:
            self.alerts_label.setText('⚠️ Network connection failed')
        else:
            self.alerts_label.setText(f'⚠️ Error: {error_msg[:50]}...')
    
    def show_general_error(self, error_msg):
        """Show general error"""
        self.connection_status_label.setText('❌ Error')
        self.connection_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #f44336;
            }
        """)
        
        self.alerts_label.setText(f'⚠️ System error: {error_msg[:50]}...')
    
    def configure_alerts(self):
        """Open connections settings to configure alerts"""
        QMessageBox.information(self, 'Configure Alerts', 
                              'Redirecting to Settings → Connections to configure alert thresholds.')
        self.main_window.show_screen('settings_connections')
    
    def closeEvent(self, event):
        """Clean up when screen closes"""
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        event.accept()
    
    def go_back(self):
        """Return to home screen"""
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        self.main_window.show_screen('home')