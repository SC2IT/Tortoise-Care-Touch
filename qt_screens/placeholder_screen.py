"""
Placeholder screen for features not yet implemented
"""

from PySide6.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QTextEdit)
from PySide6.QtCore import Qt
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

class PlaceholderScreen(BaseScreen):
    """Generic placeholder screen for unimplemented features"""
    
    def __init__(self, db_manager, main_window, feature_name, description, features_list=None):
        self.feature_name = feature_name
        self.description = description
        self.features_list = features_list or []
        super().__init__(db_manager, main_window)
        
    def build_ui(self):
        """Build placeholder screen UI"""
        # Header with back button
        header = self.create_header(f'{self.feature_name}', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Main content area
        content_area = QVBoxLayout()
        
        # Coming soon message
        coming_soon = QLabel('🚧 Coming Soon!')
        coming_soon.setAlignment(Qt.AlignCenter)
        coming_soon.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #FF9800;
                margin: 20px;
                padding: 20px;
                background-color: #FFF3E0;
                border-radius: 10px;
                border: 2px solid #FF9800;
            }
        """)
        content_area.addWidget(coming_soon)
        
        # Description
        desc_label = QLabel(self.description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #424242;
                margin: 10px 20px;
                padding: 15px;
                background-color: #F5F5F5;
                border-radius: 8px;
            }
        """)
        content_area.addWidget(desc_label)
        
        # Features list if provided
        if self.features_list:
            features_title = QLabel('Planned Features:')
            features_title.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #2E7D32;
                    margin: 20px 20px 10px 20px;
                }
            """)
            content_area.addWidget(features_title)
            
            features_text = QTextEdit()
            features_text.setPlainText('\n'.join(f'• {feature}' for feature in self.features_list))
            features_text.setReadOnly(True)
            features_text.setMaximumHeight(200)
            features_text.setStyleSheet("""
                QTextEdit {
                    font-size: 14px;
                    color: #424242;
                    background-color: #E8F5E8;
                    border: 1px solid #4CAF50;
                    border-radius: 5px;
                    padding: 10px;
                    margin: 0px 20px;
                }
            """)
            content_area.addWidget(features_text)
        
        # Status message
        status_label = QLabel('This feature is in development and will be available in a future update.')
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setWordWrap(True)
        status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666;
                margin: 20px;
                padding: 15px;
                font-style: italic;
            }
        """)
        content_area.addWidget(status_label)
        
        # Add stretch to center content
        content_area.addStretch()
        
        self.main_layout.addLayout(content_area)