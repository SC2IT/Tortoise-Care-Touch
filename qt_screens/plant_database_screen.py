"""
Plant Database Screen - Browse and search plant database with safety information

Plant data sources:
- The Tortoise Table (thetortoisetable.org.uk) - Primary safety classifications
- Atlas NBN - UK biodiversity data
- GBIF Backbone - Global biodiversity database  
- Plants of the World Online - Kew Gardens botanical database
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QLineEdit, QScrollArea, QWidget, QMessageBox,
                              QComboBox, QTextEdit, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

class PlantDatabaseScreen(BaseScreen):
    """Plant database browsing and search screen"""
    
    def __init__(self, db_manager, main_window):
        # Initialize attributes before calling parent __init__
        # because parent calls build_ui() which uses these attributes
        self.current_plants = []
        self.plants_per_page = 20
        self.current_page = 0
        self.total_plants = 0
        
        super().__init__(db_manager, main_window)
        
    def build_ui(self):
        """Build plant database UI"""
        # Header
        header = self.create_header('🌿 Plant Database', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Search and filter section
        self.create_search_section()
        
        # Stats section
        self.create_stats_section()
        
        # Main content area with scroll
        self.create_content_area()
        
        # Navigation controls
        self.create_navigation_controls()
        
        # Load initial data
        self.load_plants()
    
    def create_search_section(self):
        """Create search and filter controls"""
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin: 5px 0px;
                padding: 10px;
            }
        """)
        
        search_layout = QVBoxLayout(search_frame)
        
        # Search box
        search_row = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search plants by name or scientific name...')
        self.search_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        self.search_input.textChanged.connect(self.on_search_changed)
        search_row.addWidget(self.search_input, 3)
        
        # Safety filter
        self.safety_filter = QComboBox()
        self.safety_filter.addItems(['All Plants', 'Safe Only', 'Caution', 'Toxic Only'])
        self.safety_filter.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
        """)
        self.safety_filter.currentTextChanged.connect(self.on_filter_changed)
        search_row.addWidget(self.safety_filter, 1)
        
        # Search button
        search_btn = create_icon_button('search', 'Search', (20, 20), self.load_plants)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        search_row.addWidget(search_btn)
        
        search_layout.addLayout(search_row)
        self.main_layout.addWidget(search_frame)
    
    def create_stats_section(self):
        """Create statistics display"""
        self.stats_label = QLabel('Loading plant database...')
        self.stats_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666;
                padding: 5px 10px;
                font-weight: bold;
            }
        """)
        self.main_layout.addWidget(self.stats_label)
    
    def create_content_area(self):
        """Create scrollable content area for plants"""
        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(5)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        
        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)
    
    def create_navigation_controls(self):
        """Create pagination controls"""
        nav_layout = QHBoxLayout()
        
        # Previous button
        self.prev_btn = create_icon_button('chevron-left', 'Previous', (20, 20), self.previous_page)
        self.prev_btn.setStyleSheet(self.get_nav_button_style())
        self.prev_btn.setEnabled(False)
        nav_layout.addWidget(self.prev_btn)
        
        # Page info
        self.page_label = QLabel('Page 1 of 1')
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #666;
                padding: 8px;
            }
        """)
        nav_layout.addWidget(self.page_label, 1)
        
        # Next button
        self.next_btn = create_icon_button('chevron-right', 'Next', (20, 20), self.next_page)
        self.next_btn.setStyleSheet(self.get_nav_button_style())
        self.next_btn.setEnabled(False)
        nav_layout.addWidget(self.next_btn)
        
        self.main_layout.addLayout(nav_layout)
    
    def get_nav_button_style(self):
        """Get navigation button styling"""
        return """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover:enabled {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """
    
    def on_search_changed(self):
        """Handle search text changes with debounce"""
        # Reset to first page when searching
        self.current_page = 0
        if hasattr(self, 'search_timer'):
            self.search_timer.stop()
        
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.load_plants)
        self.search_timer.start(500)  # 500ms debounce
    
    def on_filter_changed(self):
        """Handle filter changes"""
        self.current_page = 0
        self.load_plants()
    
    def load_plants(self):
        """Load plants based on current search and filter"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            # Build query based on filters
            base_query = "FROM plants WHERE 1=1"
            params = []
            
            # Search filter
            search_text = self.search_input.text().strip()
            if search_text:
                base_query += " AND (name LIKE ? OR scientific_name LIKE ?)"
                search_param = f"%{search_text}%"
                params.extend([search_param, search_param])
            
            # Safety filter
            safety_filter = self.safety_filter.currentText()
            if safety_filter == 'Safe Only':
                base_query += " AND safety_level = 'safe'"
            elif safety_filter == 'Caution':
                base_query += " AND safety_level = 'caution'"
            elif safety_filter == 'Toxic Only':
                base_query += " AND safety_level = 'toxic'"
            
            # Get total count
            count_query = f"SELECT COUNT(*) {base_query}"
            cursor.execute(count_query, params)
            self.total_plants = cursor.fetchone()[0]
            
            # Get plants for current page
            offset = self.current_page * self.plants_per_page
            data_query = f"""
                SELECT name, scientific_name, safety_level, nutrition_notes, 
                       feeding_frequency, description, main_photo_path
                {base_query}
                ORDER BY safety_level DESC, name ASC
                LIMIT ? OFFSET ?
            """
            cursor.execute(data_query, params + [self.plants_per_page, offset])
            self.current_plants = cursor.fetchall()
            
            self.update_display()
            
        except Exception as e:
            QMessageBox.critical(self, 'Database Error', f'Failed to load plants:\n{str(e)}')
    
    def update_display(self):
        """Update the display with current plants"""
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        # Update stats
        start_idx = self.current_page * self.plants_per_page + 1
        end_idx = min(start_idx + len(self.current_plants) - 1, self.total_plants)
        self.stats_label.setText(
            f'Showing {start_idx}-{end_idx} of {self.total_plants} plants'
        )
        
        # Add plant cards
        if not self.current_plants:
            no_results = QLabel('No plants found matching your criteria.')
            no_results.setAlignment(Qt.AlignCenter)
            no_results.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #666;
                    padding: 40px;
                }
            """)
            self.content_layout.addWidget(no_results)
        else:
            for plant in self.current_plants:
                plant_card = self.create_plant_card(plant)
                self.content_layout.addWidget(plant_card)
        
        # Add stretch
        self.content_layout.addStretch()
        
        # Update navigation
        self.update_navigation()
    
    def create_plant_card(self, plant):
        """Create a card widget for a plant"""
        name, scientific_name, safety_level, nutrition_notes, feeding_frequency, description, photo_path = plant
        
        card = QFrame()
        
        # Safety level colors
        safety_colors = {
            'safe': {'bg': '#E8F5E8', 'border': '#4CAF50', 'text': '#2E7D32'},
            'caution': {'bg': '#FFF3E0', 'border': '#FF9800', 'text': '#E65100'},
            'toxic': {'bg': '#FFEBEE', 'border': '#f44336', 'text': '#C62828'}
        }
        
        colors = safety_colors.get(safety_level, safety_colors['safe'])
        
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {colors['bg']};
                border: 2px solid {colors['border']};
                border-radius: 8px;
                margin: 2px;
                padding: 10px;
            }}
        """)
        
        # Main layout - horizontal with photo and content
        main_layout = QHBoxLayout(card)
        main_layout.setSpacing(10)
        
        # Photo section
        photo_widget = self.create_photo_widget(photo_path, name)
        main_layout.addWidget(photo_widget)
        
        # Content section
        content_layout = QVBoxLayout()
        content_layout.setSpacing(5)
        
        # Header row with name and safety level
        header_layout = QHBoxLayout()
        
        # Plant name
        name_label = QLabel(name)
        name_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {colors['text']};
            }}
        """)
        header_layout.addWidget(name_label, 1)
        
        # Safety badge
        safety_badge = QLabel(safety_level.upper())
        safety_badge.setAlignment(Qt.AlignCenter)
        safety_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {colors['border']};
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 12px;
                min-width: 60px;
            }}
        """)
        header_layout.addWidget(safety_badge)
        
        content_layout.addLayout(header_layout)
        
        # Scientific name
        if scientific_name:
            sci_label = QLabel(f"<i>{scientific_name}</i>")
            sci_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 12px;
                    color: {colors['text']};
                    margin-bottom: 5px;
                }}
            """)
            content_layout.addWidget(sci_label)
        
        # Details
        details = []
        if feeding_frequency:
            details.append(f"<b>Frequency:</b> {feeding_frequency}")
        if nutrition_notes:
            details.append(f"<b>Notes:</b> {nutrition_notes}")
        if description:
            details.append(f"<b>Description:</b> {description}")
        
        if details:
            details_text = "<br>".join(details)
            details_label = QLabel(details_text)
            details_label.setWordWrap(True)
            details_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 12px;
                    color: {colors['text']};
                    line-height: 1.3;
                }}
            """)
            content_layout.addWidget(details_label)
        
        # Add content layout to main layout
        main_layout.addLayout(content_layout, 1)  # Give content more space
        
        return card
    
    def create_photo_widget(self, photo_path, plant_name):
        """Create photo widget for plant card"""
        photo_label = QLabel()
        photo_label.setFixedSize(80, 80)
        photo_label.setAlignment(Qt.AlignCenter)
        photo_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
        """)
        
        if photo_path:
            try:
                from pathlib import Path
                photo_file = Path(photo_path)
                if photo_file.exists():
                    pixmap = QPixmap(str(photo_file))
                    if not pixmap.isNull():
                        # Scale pixmap to fit while maintaining aspect ratio
                        scaled_pixmap = pixmap.scaled(76, 76, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        photo_label.setPixmap(scaled_pixmap)
                        return photo_label
            except Exception as e:
                print(f"Error loading photo for {plant_name}: {e}")
        
        # Show placeholder if no photo
        photo_label.setText("📷\nNo Photo")
        photo_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
                color: #999;
                font-size: 10px;
            }
        """)
        
        return photo_label
    
    def update_navigation(self):
        """Update pagination controls"""
        total_pages = max(1, (self.total_plants + self.plants_per_page - 1) // self.plants_per_page)
        current_page_display = self.current_page + 1
        
        self.page_label.setText(f'Page {current_page_display} of {total_pages}')
        
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < total_pages - 1)
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_plants()
    
    def next_page(self):
        """Go to next page"""
        total_pages = (self.total_plants + self.plants_per_page - 1) // self.plants_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.load_plants()
    
    def go_back(self):
        """Return to home screen"""
        self.main_window.show_screen('home')