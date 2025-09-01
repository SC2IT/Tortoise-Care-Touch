"""
Main settings screen with category navigation
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QMessageBox)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

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
                lambda screen=category['screen']: self.go_to_section(screen)
            )
            button.setMinimumHeight(80)
            
            # Apply category-specific styling
            if category['style'] == 'primary':
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
                    QPushButton:hover { background-color: #45a049; }
                    QPushButton:pressed { background-color: #3d8b40; }
                """)
            elif category['style'] == 'warning':
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
                    QPushButton:hover { background-color: #F57C00; }
                    QPushButton:pressed { background-color: #E65100; }
                """)
            elif category['style'] == 'secondary':
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
                    QPushButton:hover { background-color: #1976D2; }
                    QPushButton:pressed { background-color: #1565C0; }
                """)
            else:  # default
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #757575;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 10px;
                        font-weight: bold;
                        font-size: 16px;
                        text-align: left;
                        padding-left: 20px;
                    }
                    QPushButton:hover { background-color: #616161; }
                    QPushButton:pressed { background-color: #424242; }
                """)
            
            category_layout.addWidget(button)
            
            # Subtitle
            subtitle = QLabel(category['subtitle'])
            subtitle.setAlignment(Qt.AlignCenter)
            subtitle.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 12px;
                    margin: 2px 10px 10px 10px;
                }
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
            version_text = 'v0.3.0-qt'  # Fallback
            
        # Version label
        version_label = QLabel(f'Version: {version_text}')
        version_label.setStyleSheet("color: #888; font-size: 11px;")
        
        # Status label
        status_label = QLabel('Status: Running PySide6 on Pi Touch Display')
        status_label.setStyleSheet("color: #888; font-size: 11px;")
        
        info_layout.addWidget(version_label)
        info_layout.addStretch()
        info_layout.addWidget(status_label)
        
        self.main_layout.addLayout(info_layout)
        
    def go_to_section(self, screen_name):
        """Navigate to a specific settings section"""
        if screen_name == 'settings_users':
            # Navigate to user management screen (when implemented)
            self.show_coming_soon('User Management')
        else:
            section_name = screen_name.replace('settings_', '').replace('_', ' ').title()
            self.show_coming_soon(section_name)
            
    def show_coming_soon(self, section_name):
        """Show coming soon message for unimplemented sections"""
        msg = QMessageBox(self)
        msg.setWindowTitle('Coming Soon')
        msg.setText(f'The {section_name} section will be implemented soon!')
        msg.setIcon(QMessageBox.Information)
        
        # Style the message box for touch interface
        msg.setStyleSheet("""
            QMessageBox {
                font-size: 14px;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 40px;
                font-size: 12px;
            }
        """)
        
        msg.exec()