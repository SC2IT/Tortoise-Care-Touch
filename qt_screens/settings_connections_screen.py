"""
Connections Settings Screen - Configure Adafruit.IO, sensors, and network settings
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QLineEdit, QScrollArea, QWidget, QMessageBox,
                              QDialog, QFormLayout, QDialogButtonBox, QComboBox, 
                              QSpinBox, QTextEdit, QGroupBox, QCheckBox)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

class AdafruitIOConfigDialog(QDialog):
    """Dialog for configuring Adafruit.IO settings"""
    
    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        self.setWindowTitle('Adafruit.IO Configuration')
        self.setMinimumSize(500, 400)
        self.setModal(True)
        
        self.current_settings = current_settings or {}
        
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel("""Configure your Adafruit.IO account settings for remote sensor monitoring.

Visit io.adafruit.com to create an account and get your API key.""")
        instructions.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666;
                padding: 10px;
                background-color: #e3f2fd;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Your Adafruit.IO username')
        self.username_input.setText(self.current_settings.get('adafruit_io_username', ''))
        self.username_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)
        form_layout.addRow('Username *:', self.username_input)
        
        # API Key
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText('Your Adafruit.IO API Key')
        self.api_key_input.setText(self.current_settings.get('adafruit_io_key', ''))
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setStyleSheet(self.username_input.styleSheet())
        form_layout.addRow('API Key *:', self.api_key_input)
        
        # Show/Hide API key
        show_key_checkbox = QCheckBox('Show API Key')
        show_key_checkbox.stateChanged.connect(
            lambda state: self.api_key_input.setEchoMode(
                QLineEdit.Normal if state else QLineEdit.Password
            )
        )
        form_layout.addRow('', show_key_checkbox)
        
        layout.addLayout(form_layout)
        
        # Feed Configuration
        feeds_group = QGroupBox('Feed Configuration')
        feeds_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin: 10px 0;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        feeds_layout = QFormLayout(feeds_group)
        
        # Temperature feed
        self.temp_feed_input = QLineEdit()
        self.temp_feed_input.setPlaceholderText('temperature')
        self.temp_feed_input.setText(self.current_settings.get('temp_feed_name', 'temperature'))
        self.temp_feed_input.setStyleSheet(self.username_input.styleSheet())
        feeds_layout.addRow('Temperature Feed:', self.temp_feed_input)
        
        # Humidity feed
        self.humidity_feed_input = QLineEdit()
        self.humidity_feed_input.setPlaceholderText('humidity')
        self.humidity_feed_input.setText(self.current_settings.get('humidity_feed_name', 'humidity'))
        self.humidity_feed_input.setStyleSheet(self.username_input.styleSheet())
        feeds_layout.addRow('Humidity Feed:', self.humidity_feed_input)
        
        layout.addWidget(feeds_group)
        
        # Alert Thresholds
        thresholds_group = QGroupBox('Alert Thresholds')
        thresholds_group.setStyleSheet(feeds_group.styleSheet())
        thresholds_layout = QFormLayout(thresholds_group)
        
        # Temperature range
        temp_layout = QHBoxLayout()
        self.temp_min_input = QSpinBox()
        self.temp_min_input.setRange(-10, 50)
        self.temp_min_input.setValue(int(self.current_settings.get('temp_min', 20)))
        self.temp_min_input.setSuffix('°C')
        self.temp_max_input = QSpinBox()
        self.temp_max_input.setRange(-10, 50)
        self.temp_max_input.setValue(int(self.current_settings.get('temp_max', 35)))
        self.temp_max_input.setSuffix('°C')
        
        temp_layout.addWidget(QLabel('Min:'))
        temp_layout.addWidget(self.temp_min_input)
        temp_layout.addWidget(QLabel('Max:'))
        temp_layout.addWidget(self.temp_max_input)
        temp_layout.addStretch()
        
        thresholds_layout.addRow('Temperature Range:', temp_layout)
        
        # Humidity range
        humidity_layout = QHBoxLayout()
        self.humidity_min_input = QSpinBox()
        self.humidity_min_input.setRange(0, 100)
        self.humidity_min_input.setValue(int(self.current_settings.get('humidity_min', 60)))
        self.humidity_min_input.setSuffix('%')
        self.humidity_max_input = QSpinBox()
        self.humidity_max_input.setRange(0, 100)
        self.humidity_max_input.setValue(int(self.current_settings.get('humidity_max', 80)))
        self.humidity_max_input.setSuffix('%')
        
        humidity_layout.addWidget(QLabel('Min:'))
        humidity_layout.addWidget(self.humidity_min_input)
        humidity_layout.addWidget(QLabel('Max:'))
        humidity_layout.addWidget(self.humidity_max_input)
        humidity_layout.addStretch()
        
        thresholds_layout.addRow('Humidity Range:', humidity_layout)
        
        layout.addWidget(thresholds_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Test connection button
        test_btn = QPushButton('Test Connection')
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        test_btn.clicked.connect(self.test_connection)
        button_layout.addWidget(test_btn)
        
        button_layout.addStretch()
        
        # Standard buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("""
            QDialogButtonBox QPushButton {
                font-size: 12px;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                min-width: 80px;
            }
            QDialogButtonBox QPushButton[text="OK"] {
                background-color: #4CAF50;
                color: white;
            }
            QDialogButtonBox QPushButton[text="OK"]:hover {
                background-color: #45a049;
            }
            QDialogButtonBox QPushButton[text="Cancel"] {
                background-color: #757575;
                color: white;
            }
            QDialogButtonBox QPushButton[text="Cancel"]:hover {
                background-color: #616161;
            }
        """)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_layout.addWidget(button_box)
        
        layout.addLayout(button_layout)
    
    def test_connection(self):
        """Test Adafruit.IO connection"""
        username = self.username_input.text().strip()
        api_key = self.api_key_input.text().strip()
        
        if not username or not api_key:
            QMessageBox.warning(self, 'Missing Information', 
                              'Please enter both username and API key before testing.')
            return
        
        try:
            # Import and test Adafruit.IO connection
            from Adafruit_IO import Client
            aio = Client(username, api_key)
            
            # Try to get user info to test connection
            user_info = aio.receive_data('test-feed')  # This will fail gracefully if feed doesn't exist
            
            QMessageBox.information(self, 'Connection Successful', 
                                  'Successfully connected to Adafruit.IO!')
            
        except ImportError:
            QMessageBox.warning(self, 'Missing Library', 
                              'Adafruit.IO library not installed.\n\n'
                              'Install with: pip install adafruit-circuitpython-io')
        except Exception as e:
            error_msg = str(e)
            if 'Unauthorized' in error_msg or '401' in error_msg:
                QMessageBox.critical(self, 'Authentication Failed', 
                                   'Invalid username or API key.\n\n'
                                   'Please check your Adafruit.IO credentials.')
            elif 'Network' in error_msg or 'Connection' in error_msg:
                QMessageBox.critical(self, 'Network Error', 
                                   'Unable to connect to Adafruit.IO.\n\n'
                                   'Please check your internet connection.')
            else:
                QMessageBox.information(self, 'Connection Test', 
                                      f'Connection appears to be working.\n\n'
                                      f'Note: {error_msg}')
    
    def get_settings(self):
        """Get configuration settings from form"""
        return {
            'adafruit_io_username': self.username_input.text().strip(),
            'adafruit_io_key': self.api_key_input.text().strip(),
            'temp_feed_name': self.temp_feed_input.text().strip() or 'temperature',
            'humidity_feed_name': self.humidity_feed_input.text().strip() or 'humidity',
            'temp_min': str(self.temp_min_input.value()),
            'temp_max': str(self.temp_max_input.value()),
            'humidity_min': str(self.humidity_min_input.value()),
            'humidity_max': str(self.humidity_max_input.value())
        }

class SettingsConnectionsScreen(BaseScreen):
    """Connections and Network Settings Screen"""
    
    def build_ui(self):
        """Build connections settings UI"""
        # Header
        header = self.create_header('🌐 Connections & Sensors', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Create connection sections
        self.create_adafruit_section()
        self.create_sensor_section()
        self.create_network_section()
        
    def create_adafruit_section(self):
        """Create Adafruit.IO configuration section"""
        # Section title
        section_title = QLabel('🌡️ Adafruit.IO Integration')
        section_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2196F3;
                margin: 10px 5px;
                padding: 5px;
            }
        """)
        self.main_layout.addWidget(section_title)
        
        # Configuration card
        config_widget = QWidget()
        config_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                margin: 5px;
            }
        """)
        
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(20, 20, 20, 20)
        
        # Status info
        self.adafruit_status_label = QLabel('Checking connection status...')
        self.adafruit_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666;
                margin-bottom: 10px;
            }
        """)
        config_layout.addWidget(self.adafruit_status_label)
        
        # Description
        desc_label = QLabel(
            'Configure Adafruit.IO integration for remote temperature and humidity monitoring. '
            'This allows you to view sensor data from anywhere and receive alerts when '
            'habitat conditions are outside safe ranges.'
        )
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #777;
                margin-bottom: 15px;
            }
        """)
        desc_label.setWordWrap(True)
        config_layout.addWidget(desc_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Configure button
        configure_btn = create_icon_button('settings', 'Configure Adafruit.IO', (20, 20), self.configure_adafruit)
        configure_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #1565C0; }
        """)
        configure_btn.setMinimumHeight(50)
        button_layout.addWidget(configure_btn)
        
        # Test connection button
        test_btn = create_icon_button('activity', 'Test Connection', (20, 20), self.test_adafruit_connection)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover { background-color: #F57C00; }
            QPushButton:pressed { background-color: #E65100; }
        """)
        test_btn.setMinimumHeight(50)
        test_btn.setMaximumWidth(200)
        button_layout.addWidget(test_btn)
        
        config_layout.addLayout(button_layout)
        self.main_layout.addWidget(config_widget)
        
        # Update status
        self.update_adafruit_status()
    
    def create_sensor_section(self):
        """Create local sensor configuration section"""
        # Section title
        section_title = QLabel('🔧 Local Sensors')
        section_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #4CAF50;
                margin: 20px 5px 10px 5px;
                padding: 5px;
            }
        """)
        self.main_layout.addWidget(section_title)
        
        # Sensor info card
        sensor_widget = QWidget()
        sensor_widget.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                margin: 5px;
            }
        """)
        
        sensor_layout = QVBoxLayout(sensor_widget)
        sensor_layout.setContentsMargins(20, 20, 20, 20)
        
        # Coming soon message
        coming_soon_label = QLabel('🚧 Local sensor configuration coming soon!')
        coming_soon_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #FF9800;
                margin-bottom: 10px;
            }
        """)
        sensor_layout.addWidget(coming_soon_label)
        
        # Description
        sensor_desc = QLabel(
            'Future features will include:\n'
            '• DHT22/AM2302 temperature/humidity sensor support\n'
            '• GPIO pin configuration for Raspberry Pi\n'
            '• Local data logging and backup\n'
            '• Calibration and sensor testing tools'
        )
        sensor_desc.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666;
            }
        """)
        sensor_layout.addWidget(sensor_desc)
        
        self.main_layout.addWidget(sensor_widget)
    
    def create_network_section(self):
        """Create network settings section"""
        # Section title
        section_title = QLabel('📡 Network Settings')
        section_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #9C27B0;
                margin: 20px 5px 10px 5px;
                padding: 5px;
            }
        """)
        self.main_layout.addWidget(section_title)
        
        # Network info card
        network_widget = QWidget()
        network_widget.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                margin: 5px;
            }
        """)
        
        network_layout = QVBoxLayout(network_widget)
        network_layout.setContentsMargins(20, 20, 20, 20)
        
        # Coming soon message
        network_label = QLabel('🚧 Network settings coming soon!')
        network_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #FF9800;
                margin-bottom: 10px;
            }
        """)
        network_layout.addWidget(network_label)
        
        # Description
        network_desc = QLabel(
            'Future features will include:\n'
            '• Wi-Fi configuration for Raspberry Pi\n'
            '• Emergency veterinarian contact management\n'
            '• Remote access settings\n'
            '• Data sync and backup options'
        )
        network_desc.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666;
            }
        """)
        network_layout.addWidget(network_desc)
        
        self.main_layout.addWidget(network_widget)
        
    def update_adafruit_status(self):
        """Update Adafruit.IO connection status"""
        try:
            # Get current settings from database
            settings = {}
            if hasattr(self.db_manager, 'get_setting'):
                username = self.db_manager.get_setting('adafruit_io_username')
                api_key = self.db_manager.get_setting('adafruit_io_key')
                
                if username and api_key:
                    settings['adafruit_io_username'] = username
                    settings['adafruit_io_key'] = api_key
            
            if settings.get('adafruit_io_username') and settings.get('adafruit_io_key'):
                self.adafruit_status_label.setText('✅ Adafruit.IO configured - Click "Test Connection" to verify')
                self.adafruit_status_label.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        color: #4CAF50;
                        margin-bottom: 10px;
                        font-weight: bold;
                    }
                """)
            else:
                self.adafruit_status_label.setText('⚠️ Adafruit.IO not configured - Click "Configure" to set up')
                self.adafruit_status_label.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        color: #FF9800;
                        margin-bottom: 10px;
                        font-weight: bold;
                    }
                """)
        except Exception:
            self.adafruit_status_label.setText('❌ Unable to check configuration status')
            self.adafruit_status_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #f44336;
                    margin-bottom: 10px;
                    font-weight: bold;
                }
            """)
    
    def configure_adafruit(self):
        """Open Adafruit.IO configuration dialog"""
        # Get current settings
        current_settings = {}
        try:
            if hasattr(self.db_manager, 'get_all_settings'):
                current_settings = self.db_manager.get_all_settings()
            else:
                # Fallback: try to get individual settings
                settings_keys = ['adafruit_io_username', 'adafruit_io_key', 'temp_feed_name', 
                               'humidity_feed_name', 'temp_min', 'temp_max', 'humidity_min', 'humidity_max']
                for key in settings_keys:
                    try:
                        value = self.db_manager.get_setting(key)
                        if value:
                            current_settings[key] = value
                    except:
                        pass
        except Exception:
            pass
        
        dialog = AdafruitIOConfigDialog(self, current_settings)
        
        if dialog.exec() == QDialog.Accepted:
            settings = dialog.get_settings()
            try:
                # Save settings to database
                for key, value in settings.items():
                    if hasattr(self.db_manager, 'set_setting'):
                        self.db_manager.set_setting(key, value)
                    else:
                        # Fallback: try direct database update
                        self.update_setting_direct(key, value)
                
                QMessageBox.information(self, 'Settings Saved', 
                                      'Adafruit.IO configuration saved successfully!')
                
                # Update status
                self.update_adafruit_status()
                
            except Exception as e:
                QMessageBox.critical(self, 'Error', 
                                   f'Failed to save settings: {str(e)}')
    
    def update_setting_direct(self, key, value):
        """Direct database update for settings (fallback method)"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at) 
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        conn.commit()
    
    def test_adafruit_connection(self):
        """Test Adafruit.IO connection with current settings"""
        try:
            # Get current settings
            username = None
            api_key = None
            
            if hasattr(self.db_manager, 'get_setting'):
                username = self.db_manager.get_setting('adafruit_io_username')
                api_key = self.db_manager.get_setting('adafruit_io_key')
            else:
                # Fallback: direct database query
                conn = self.db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT value FROM settings WHERE key = ?', ('adafruit_io_username',))
                row = cursor.fetchone()
                username = row[0] if row else None
                
                cursor.execute('SELECT value FROM settings WHERE key = ?', ('adafruit_io_key',))
                row = cursor.fetchone()
                api_key = row[0] if row else None
            
            if not username or not api_key:
                QMessageBox.warning(self, 'Configuration Missing', 
                                  'Please configure Adafruit.IO settings first.')
                return
            
            # Test connection
            from Adafruit_IO import Client
            aio = Client(username, api_key)
            
            # Try to get a feed list (this will verify connection)
            feeds = aio.feeds()
            
            QMessageBox.information(self, 'Connection Successful', 
                                  f'Successfully connected to Adafruit.IO!\n\n'
                                  f'Found {len(feeds)} feeds in your account.')
            
        except ImportError:
            QMessageBox.warning(self, 'Missing Library', 
                              'Adafruit.IO library not installed.\n\n'
                              'Install with: pip install adafruit-circuitpython-io')
        except Exception as e:
            error_msg = str(e)
            if 'Unauthorized' in error_msg or '401' in error_msg:
                QMessageBox.critical(self, 'Authentication Failed', 
                                   'Invalid username or API key.\n\n'
                                   'Please check your Adafruit.IO credentials.')
            elif 'Network' in error_msg or 'Connection' in error_msg:
                QMessageBox.critical(self, 'Network Error', 
                                   'Unable to connect to Adafruit.IO.\n\n'
                                   'Please check your internet connection.')
            else:
                QMessageBox.critical(self, 'Connection Error', f'Connection failed:\n\n{error_msg}')
    
    def go_back(self):
        """Return to settings main screen"""
        self.main_window.show_screen('settings_main')