"""
Tortoise Selection Screen
Shows tortoises with photos and descriptions for care entry selection
"""

import os
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QScrollArea, QWidget, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

class TortoiseSelectionScreen(BaseScreen):
    """Screen for selecting a tortoise before care entry"""
    
    def __init__(self, db_manager, main_window, return_screen='home', action_name='Care Entry'):
        self.return_screen = return_screen
        self.action_name = action_name
        self.selected_tortoise_id = None
        super().__init__(db_manager, main_window)
        
    def build_ui(self):
        """Build tortoise selection UI"""
        # Header with back button
        header = self.create_header(f'🐢 Select Tortoise for {self.action_name}', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Instructions
        instructions = QLabel('Select the tortoise you want to work with:')
        instructions.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666;
                margin: 10px 0;
                text-align: center;
            }
        """)
        instructions.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(instructions)
        
        # Scroll area for tortoise cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container widget for tortoise cards
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        
        scroll.setWidget(self.scroll_widget)
        self.main_layout.addWidget(scroll)
        
        # Load tortoises
        self.load_tortoises()
        
    def load_tortoises(self):
        """Load and display all tortoises"""
        # Clear existing tortoise cards
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Get tortoises from database
        tortoises = self.db_manager.get_all_tortoises()
        
        if not tortoises:
            no_tortoises_label = QLabel('No tortoises found. Please add tortoises in Settings > Tortoise Management first.')
            no_tortoises_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #666;
                    padding: 20px;
                    text-align: center;
                }
            """)
            no_tortoises_label.setAlignment(Qt.AlignCenter)
            no_tortoises_label.setWordWrap(True)
            self.scroll_layout.addWidget(no_tortoises_label)
            return
            
        # Create tortoise cards
        for tortoise in tortoises:
            card = self.create_tortoise_card(tortoise)
            self.scroll_layout.addWidget(card)
            
        # Add stretch to push cards to top
        self.scroll_layout.addStretch()
        
    def create_tortoise_card(self, tortoise):
        """Create a tortoise selection card with photo and info"""
        # Main card frame
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 10px;
                margin: 5px;
                padding: 0px;
            }
            QFrame:hover {
                border-color: #4CAF50;
                background-color: #f8fff8;
            }
        """)
        card.setMinimumHeight(120)
        card.setMaximumHeight(180)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Photo section
        photo_widget = QWidget()
        photo_widget.setFixedSize(100, 100)
        photo_layout = QVBoxLayout(photo_widget)
        photo_layout.setContentsMargins(0, 0, 0, 0)
        
        photo_label = QLabel()
        photo_label.setFixedSize(90, 90)
        photo_label.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f5f5f5;
            }
        """)
        photo_label.setAlignment(Qt.AlignCenter)
        
        # Load photo if available
        if tortoise.get('photo_path') and os.path.exists(tortoise['photo_path']):
            try:
                pixmap = QPixmap(tortoise['photo_path'])
                if not pixmap.isNull():
                    # Scale to fill entire space
                    scaled_pixmap = pixmap.scaled(88, 88, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    photo_label.setPixmap(scaled_pixmap)
                    photo_label.setScaledContents(True)  # Fill entire space
                else:
                    photo_label.setText('📷\nNo Photo')
                    photo_label.setStyleSheet(photo_label.styleSheet() + "color: #999; font-size: 10px;")
            except Exception as e:
                print(f"Error loading photo {tortoise['photo_path']}: {e}")
                photo_label.setText('📷\nError')
                photo_label.setStyleSheet(photo_label.styleSheet() + "color: #999; font-size: 10px;")
        else:
            photo_label.setText('📷\nNo Photo')
            photo_label.setStyleSheet(photo_label.styleSheet() + "color: #999; font-size: 10px;")
        
        photo_layout.addWidget(photo_label)
        layout.addWidget(photo_widget)
        
        # Info section
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)
        
        # Tortoise name
        name_label = QLabel(tortoise['name'])
        name_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2E7D32;
                margin-bottom: 5px;
            }
        """)
        info_layout.addWidget(name_label)
        
        # Species and details
        details = []
        if tortoise.get('species'):
            details.append(tortoise['species'])
        if tortoise.get('subspecies') and tortoise['subspecies'] != 'Unknown':
            details.append(f"({tortoise['subspecies']})")
        if tortoise.get('sex') and tortoise['sex'] != 'Unknown':
            details.append(f"{tortoise['sex']}")
        
        if details:
            details_label = QLabel(' - '.join(details))
            details_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #666;
                }
            """)
            details_label.setWordWrap(True)
            info_layout.addWidget(details_label)
        
        # Physical description
        if tortoise.get('physical_description'):
            desc_text = tortoise['physical_description']
            if len(desc_text) > 80:
                desc_text = desc_text[:77] + "..."
            
            desc_label = QLabel(f"Description: {desc_text}")
            desc_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #555;
                    font-style: italic;
                    margin-top: 5px;
                }
            """)
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
        
        # Weight and age info
        extra_info = []
        if tortoise.get('current_weight'):
            extra_info.append(f"Weight: {tortoise['current_weight']}g")
        if tortoise.get('birth_date'):
            extra_info.append(f"Born: {tortoise['birth_date']}")
            
        if extra_info:
            extra_label = QLabel(' | '.join(extra_info))
            extra_label.setStyleSheet("""
                QLabel {
                    font-size: 10px;
                    color: #777;
                }
            """)
            info_layout.addWidget(extra_label)
        
        info_layout.addStretch()
        layout.addWidget(info_widget, 1)
        
        # Select button
        select_button = self.create_button(
            f'Select\n{tortoise["name"]}', 
            lambda checked=False, t_id=tortoise['id']: self.select_tortoise(t_id),
            'primary'
        )
        select_button.setFixedWidth(100)
        select_button.setMinimumHeight(90)
        layout.addWidget(select_button)
        
        return card
        
    def select_tortoise(self, tortoise_id):
        """Handle tortoise selection"""
        self.selected_tortoise_id = tortoise_id
        
        # Get tortoise details for confirmation
        tortoise = self.db_manager.get_tortoise_by_id(tortoise_id)
        if tortoise:
            # Store selection in main window for use by other screens
            self.main_window.selected_tortoise = tortoise
            
            # Determine destination screen based on action name
            if self.action_name == 'Feeding':
                self.go_to_screen('feeding')
            elif self.action_name == 'Health Records':
                self.go_to_screen('health')
            elif self.action_name == 'Care Entry':
                self.go_to_screen('care')
            else:
                # Default fallback
                self.go_to_screen(self.return_screen)
        
    def go_back(self):
        """Navigate back to the specified return screen"""
        self.go_to_screen(self.return_screen)
        
    def on_enter(self):
        """Called when screen becomes active"""
        # Refresh tortoise list
        self.load_tortoises()