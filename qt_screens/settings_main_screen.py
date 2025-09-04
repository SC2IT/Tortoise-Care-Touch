"""
Main settings screen with category navigation
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QMessageBox)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

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
        'extended': {
            'success': '#28a745',
            'warning': '#ffc107',
            'error': '#dc3545',
        }
    }

class SettingsMainScreen(BaseScreen):
    """Main settings screen with large category buttons"""
    
    def build_ui(self):
        """Build settings main screen UI"""
        # Header with back button
        header = self.create_header('Settings', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Settings category buttons
        self.create_settings_categories()
        
        # Version and status info
        self.create_info_section()
        
    def create_settings_categories(self):
        """Create settings category buttons"""
        categories = [
            {
                'title': 'User Management',
                'icon': 'users',
                'subtitle': 'Add users, assign tasks, manage profiles',
                'screen': 'settings_users',
                'style': 'primary'
            },
            {
                'title': 'Tortoise Management',
                'icon': 'tortoise',
                'subtitle': 'Add tortoises, edit profiles, view info',
                'screen': 'settings_tortoises',
                'style': 'warning'
            },
            {
                'title': 'Connections',
                'icon': 'wifi',
                'subtitle': 'Adafruit.IO, sensors, network settings',
                'screen': 'settings_connections',
                'style': 'secondary'
            },
            {
                'title': 'Database',
                'icon': 'database',
                'subtitle': 'Backup, restore, import/export data',
                'screen': 'settings_database',
                'style': 'default'
            }
        ]
        
        for category in categories:
            # Create category button container
            category_layout = QVBoxLayout()
            category_layout.setSpacing(5)
            
            # Main category button with PNG icon
            button = create_icon_button(
                category['icon'],
                category['title'], 
                (32, 32),
                None  # We'll connect the signal manually
            )
            
            # Connect button manually to avoid lambda closure issues
            def create_handler(screen_name):
                return lambda: self.go_to_section(screen_name)
            
            button.clicked.connect(create_handler(category['screen']))
            button.setMinimumHeight(90)  # Touch-friendly height
            
            # Apply category-specific styling with design system colors
            if category['style'] == 'primary':
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
                    QPushButton:hover {{ background-color: {APP_COLORS['blue_gray_family']['dark']}; }}
                    QPushButton:pressed {{ background-color: {APP_COLORS['blue_gray_family']['darker']}; }}
                """)
            elif category['style'] == 'warning':
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
                    QPushButton:hover {{ background-color: {APP_COLORS['purple_gray_family']['dark']}; }}
                    QPushButton:pressed {{ background-color: {APP_COLORS['purple_gray_family']['darker']}; }}
                """)
            elif category['style'] == 'secondary':
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
                    QPushButton:hover {{ background-color: {APP_COLORS['teal_gray_family']['dark']}; }}
                    QPushButton:pressed {{ background-color: {APP_COLORS['teal_gray_family']['darker']}; }}
                """)
            else:  # default
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {APP_COLORS['text']['secondary']};
                        color: white;
                        border: none;
                        border-radius: 12px;
                        padding: 15px;
                        font-weight: bold;
                        font-size: 18px;
                        text-align: left;
                        padding-left: 25px;
                    }}
                    QPushButton:hover {{ background-color: {APP_COLORS['text']['muted']}; }}
                    QPushButton:pressed {{ background-color: {APP_COLORS['blue_gray_family']['darker']}; }}
                """)
            
            category_layout.addWidget(button)
            
            # Subtitle
            subtitle = QLabel(category['subtitle'])
            subtitle.setAlignment(Qt.AlignCenter)
            subtitle.setStyleSheet(f"""
                QLabel {{
                    color: {APP_COLORS['text']['muted']};
                    font-size: 14px;
                    margin: 2px 10px 10px 10px;
                    font-weight: 400;
                }}
            """)
            category_layout.addWidget(subtitle)
            
            self.main_layout.addLayout(category_layout)
            
    def create_info_section(self):
        """Create version and status information section"""
        info_layout = QHBoxLayout()
        
        # Read version from VERSION file
        version_text = 'Unknown'
        try:
            import os
            version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')
            with open(version_file, 'r') as f:
                version_text = f.read().strip()
        except:
            version_text = 'v0.3.0-alpha'  # Fallback
            
        # Version label
        version_label = QLabel(f'Version: {version_text}')
        version_label.setStyleSheet(f"color: {APP_COLORS['text']['muted']}; font-size: 12px;")
        
        # Status label
        status_label = QLabel('Status: Running PySide6 on Pi Touch Display')
        status_label.setStyleSheet(f"color: {APP_COLORS['text']['muted']}; font-size: 12px;")
        
        info_layout.addWidget(version_label)
        info_layout.addStretch()
        info_layout.addWidget(status_label)
        
        self.main_layout.addLayout(info_layout)
        
    def go_to_section(self, screen_name):
        """Navigate to a specific settings section"""
        if screen_name in ['settings_users', 'settings_tortoises', 'settings_connections']:
            # Navigate to functional settings screens
            self.main_window.show_screen(screen_name)
        else:
            # Show coming soon for other sections
            section_name = screen_name.replace('settings_', '').replace('_', ' ').title()
            self.show_coming_soon(section_name)
            
    def show_coming_soon(self, section_name):
        """Show coming soon message for unimplemented sections"""
        msg = QMessageBox(self)
        msg.setWindowTitle('Coming Soon')
        msg.setText(f'The {section_name} section will be implemented soon!')
        msg.setIcon(QMessageBox.Information)
        
        # Style the message box for touch interface with design system
        msg.setStyleSheet(f"""
            QMessageBox {{
                font-size: 16px;
                background-color: {APP_COLORS['backgrounds']['white']};
            }}
            QMessageBox QPushButton {{
                min-width: 100px;
                min-height: 45px;
                font-size: 14px;
                background-color: {APP_COLORS['core']['blue_gray']};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {APP_COLORS['blue_gray_family']['dark']};
            }}
        """)
        
        msg.exec()