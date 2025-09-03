"""
Plant Database Screen - Modern Grid Layout with Touch Interface
Browse and search plant database with large photos and detailed views
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QLineEdit, QScrollArea, QWidget, QMessageBox,
                              QComboBox, QFrame, QStackedWidget)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

class PlantCard(QFrame):
    """Individual plant card widget for grid display"""
    clicked = Signal(dict)
    
    def __init__(self, plant_data):
        super().__init__()
        self.plant_data = plant_data
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the plant card UI"""
        name, sci_name, safety_level, nutrition_notes, frequency, description, photo_path = self.plant_data
        
        # Safety level colors
        colors = {
            'safe': {'bg': '#E8F5E8', 'border': '#4CAF50', 'text': '#2E7D32'},
            'caution': {'bg': '#FFF3E0', 'border': '#FF9800', 'text': '#E65100'},
            'toxic': {'bg': '#FFEBEE', 'border': '#f44336', 'text': '#C62828'}
        }
        
        color = colors.get(safety_level, colors['safe'])
        
        # Card styling - touch friendly size
        self.setFixedSize(220, 300)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color['bg']};
                border: 3px solid {color['border']};
                border-radius: 12px;
                margin: 5px;
            }}
            QFrame:hover {{
                border: 4px solid {color['border']};
                background-color: white;
                transform: scale(1.02);
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Photo area (much larger - 180x130)
        photo_label = QLabel()
        photo_label.setFixedSize(180, 130)
        photo_label.setAlignment(Qt.AlignCenter)
        photo_label.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {color['border']};
                border-radius: 8px;
                background-color: white;
            }}
        """)
        
        # Load photo
        if photo_path:
            try:
                from pathlib import Path
                photo_file = Path(photo_path)
                if photo_file.exists():
                    pixmap = QPixmap(str(photo_file))
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(176, 126, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        photo_label.setPixmap(scaled_pixmap)
                    else:
                        self.set_no_photo_placeholder(photo_label, color)
                else:
                    self.set_no_photo_placeholder(photo_label, color)
            except Exception:
                self.set_no_photo_placeholder(photo_label, color)
        else:
            self.set_no_photo_placeholder(photo_label, color)
            
        layout.addWidget(photo_label, 0, Qt.AlignCenter)
        
        # Plant name (larger, bold text)
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {color['text']};
                background-color: transparent;
                padding: 8px;
            }}
        """)
        layout.addWidget(name_label)
        
        # Safety badge (prominent)
        safety_badge = QLabel(safety_level.upper())
        safety_badge.setAlignment(Qt.AlignCenter)
        safety_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {color['border']};
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 18px;
                min-width: 100px;
            }}
        """)
        layout.addWidget(safety_badge, 0, Qt.AlignCenter)
        
        # Scientific name (smaller, italic)
        if sci_name:
            sci_label = QLabel(f"<i>{sci_name}</i>")
            sci_label.setAlignment(Qt.AlignCenter)
            sci_label.setWordWrap(True)
            sci_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 12px;
                    color: {color['text']};
                    background-color: transparent;
                    padding: 2px;
                }}
            """)
            layout.addWidget(sci_label)
            
        layout.addStretch()
        
    def set_no_photo_placeholder(self, label, color):
        """Set placeholder when no photo available"""
        label.setText("🌱\nNo Photo")
        label.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {color['border']};
                border-radius: 8px;
                background-color: white;
                color: #999;
                font-size: 14px;
            }}
        """)
        
    def mousePressEvent(self, event):
        """Handle card click - touch friendly"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.plant_data)
        super().mousePressEvent(event)

class PlantDetailView(QWidget):
    """Detailed view for individual plant with large photos"""
    back_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup detailed view UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header with back button
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Back to Plants")
        back_btn.setFixedHeight(50)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        back_btn.clicked.connect(self.back_clicked.emit)
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(20)
        scroll_area.setWidget(self.content_widget)
        
        layout.addWidget(scroll_area)
        
    def show_plant(self, plant_data):
        """Display detailed plant information"""
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
                
        name, sci_name, safety_level, nutrition_notes, frequency, description, photo_path = plant_data
        
        # Safety colors
        colors = {
            'safe': {'bg': '#E8F5E8', 'border': '#4CAF50', 'text': '#2E7D32'},
            'caution': {'bg': '#FFF3E0', 'border': '#FF9800', 'text': '#E65100'},
            'toxic': {'bg': '#FFEBEE', 'border': '#f44336', 'text': '#C62828'}
        }
        color = colors.get(safety_level, colors['safe'])
        
        # Plant header section
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {color['bg']};
                border: 4px solid {color['border']};
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        
        # Plant name (large title)
        title_label = QLabel(name)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                font-weight: bold;
                color: {color['text']};
                margin-bottom: 15px;
            }}
        """)
        header_layout.addWidget(title_label)
        
        # Scientific name and safety badge
        info_layout = QHBoxLayout()
        if sci_name:
            sci_label = QLabel(f"<i>{sci_name}</i>")
            sci_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 20px;
                    color: {color['text']};
                }}
            """)
            info_layout.addWidget(sci_label)
            
        info_layout.addStretch()
        
        safety_badge = QLabel(safety_level.upper())
        safety_badge.setAlignment(Qt.AlignCenter)
        safety_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {color['border']};
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 25px;
                min-width: 120px;
            }}
        """)
        info_layout.addWidget(safety_badge)
        header_layout.addLayout(info_layout)
        
        self.content_layout.addWidget(header_frame)
        
        # Large photo section
        self.create_photo_section(photo_path, name, color)
        
        # Plant details section
        self.create_details_section(nutrition_notes, frequency, description, color)
        
        self.content_layout.addStretch()
        
    def create_photo_section(self, photo_path, plant_name, color):
        """Create large photo display section"""
        photo_frame = QFrame()
        photo_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 3px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }
        """)
        photo_layout = QVBoxLayout(photo_frame)
        
        title = QLabel("Plant Photos")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 15px;
            }
        """)
        photo_layout.addWidget(title)
        
        # Large main photo (500x400 - much bigger!)
        photo_label = QLabel()
        photo_label.setFixedSize(500, 400)
        photo_label.setAlignment(Qt.AlignCenter)
        photo_label.setStyleSheet(f"""
            QLabel {{
                border: 3px solid {color['border']};
                border-radius: 10px;
                background-color: #f9f9f9;
            }}
        """)
        
        if photo_path:
            try:
                from pathlib import Path
                photo_file = Path(photo_path)
                if photo_file.exists():
                    pixmap = QPixmap(str(photo_file))
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(494, 394, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        photo_label.setPixmap(scaled_pixmap)
                    else:
                        self.set_large_placeholder(photo_label, plant_name)
                else:
                    self.set_large_placeholder(photo_label, plant_name)
            except Exception:
                self.set_large_placeholder(photo_label, plant_name)
        else:
            self.set_large_placeholder(photo_label, plant_name)
            
        photo_layout.addWidget(photo_label, 0, Qt.AlignCenter)
        
        # Future multiple photo support note
        note_label = QLabel("📸 Tap photo for full size • Multiple photos coming soon")
        note_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666;
                font-style: italic;
                margin-top: 15px;
            }
        """)
        photo_layout.addWidget(note_label, 0, Qt.AlignCenter)
        
        self.content_layout.addWidget(photo_frame)
        
    def set_large_placeholder(self, label, plant_name):
        """Set large placeholder image"""
        label.setText(f"🌱\n\nNo Photo Available\nfor {plant_name}")
        label.setStyleSheet("""
            QLabel {
                border: 3px solid #ddd;
                border-radius: 10px;
                background-color: #f9f9f9;
                color: #999;
                font-size: 18px;
            }
        """)
        
    def create_details_section(self, nutrition_notes, frequency, description, color):
        """Create plant details section"""
        details_frame = QFrame()
        details_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {color['bg']};
                border: 3px solid {color['border']};
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }}
        """)
        details_layout = QVBoxLayout(details_frame)
        
        title = QLabel("Plant Information")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {color['text']};
                margin-bottom: 20px;
            }}
        """)
        details_layout.addWidget(title)
        
        if frequency:
            freq_label = QLabel(f"<b>Feeding Frequency:</b> {frequency}")
            freq_label.setWordWrap(True)
            freq_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 18px;
                    color: {color['text']};
                    margin-bottom: 15px;
                    padding: 15px;
                    background-color: white;
                    border-radius: 8px;
                }}
            """)
            details_layout.addWidget(freq_label)
            
        if nutrition_notes:
            notes_label = QLabel(f"<b>Nutrition Notes:</b> {nutrition_notes}")
            notes_label.setWordWrap(True)
            notes_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 18px;
                    color: {color['text']};
                    margin-bottom: 15px;
                    padding: 15px;
                    background-color: white;
                    border-radius: 8px;
                }}
            """)
            details_layout.addWidget(notes_label)
            
        if description:
            desc_label = QLabel(f"<b>Description:</b> {description}")
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 18px;
                    color: {color['text']};
                    padding: 15px;
                    background-color: white;
                    border-radius: 8px;
                }}
            """)
            details_layout.addWidget(desc_label)
            
        self.content_layout.addWidget(details_frame)

class PlantDatabaseScreen(BaseScreen):
    """Plant database with modern grid layout and touch interface"""
    
    def __init__(self, db_manager, main_window):
        # Initialize attributes before calling parent __init__
        self.current_plants = []
        self.plants_per_page = 9  # 3x3 grid for touch interface
        self.current_page = 0
        self.total_plants = 0
        
        super().__init__(db_manager, main_window)
        
    def build_ui(self):
        """Build plant database UI with grid and detail views"""
        # Header
        header = self.create_header('🌿 Plant Database', show_back_button=True)
        self.main_layout.addLayout(header)
        
        # Create stacked widget for grid/detail views
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # Grid view page
        self.grid_page = QWidget()
        self.setup_grid_view()
        self.stack.addWidget(self.grid_page)
        
        # Detail view page
        self.detail_view = PlantDetailView()
        self.detail_view.back_clicked.connect(self.show_grid_view)
        self.stack.addWidget(self.detail_view)
        
        # Start with grid view
        self.stack.setCurrentWidget(self.grid_page)
        
        # Load initial data
        self.load_plants()
        
    def setup_grid_view(self):
        """Setup the grid view layout"""
        layout = QVBoxLayout(self.grid_page)
        layout.setSpacing(15)
        
        # Search and filter section
        self.create_search_section(layout)
        
        # Stats section
        self.create_stats_section(layout)
        
        # Grid content area
        self.create_grid_content_area(layout)
        
        # Navigation controls
        self.create_navigation_controls(layout)
    
    def create_search_section(self, parent_layout):
        """Create search and filter controls"""
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 3px solid #e0e0e0;
                border-radius: 12px;
                margin: 10px;
                padding: 15px;
            }
        """)
        
        search_layout = QVBoxLayout(search_frame)
        
        # Search box
        search_row = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search plants by name or scientific name...')
        self.search_input.setFixedHeight(45)
        self.search_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 8px;
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
        self.safety_filter.setCurrentText('All Plants')
        self.safety_filter.setFixedHeight(45)
        self.safety_filter.setStyleSheet("""
            QComboBox {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 8px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)
        self.safety_filter.currentTextChanged.connect(self.on_filter_changed)
        search_row.addWidget(self.safety_filter, 1)
        
        # Search button
        search_btn = QPushButton('🔍 Search')
        search_btn.setFixedHeight(45)
        search_btn.clicked.connect(self.load_plants)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        search_row.addWidget(search_btn)
        
        search_layout.addLayout(search_row)
        parent_layout.addWidget(search_frame)

    def create_stats_section(self, parent_layout):
        """Create statistics display"""
        self.stats_label = QLabel('Loading plant database...')
        self.stats_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666;
                padding: 8px 15px;
                font-weight: bold;
            }
        """)
        parent_layout.addWidget(self.stats_label)
    
    def create_grid_content_area(self, parent_layout):
        """Create scrollable grid content area for plants"""
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
                width: 15px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background-color: #4CAF50;
                border-radius: 7px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #45a049;
            }
        """)
        
        # Content widget for grid
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: #f8f8f8;
            }
        """)
        
        # Grid layout for plant cards (3 columns)
        self.grid_layout = QGridLayout(self.content_widget)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        
        self.scroll_area.setWidget(self.content_widget)
        parent_layout.addWidget(self.scroll_area)

    def create_navigation_controls(self, parent_layout):
        """Create pagination controls"""
        nav_frame = QFrame()
        nav_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 3px solid #e0e0e0;
                border-radius: 12px;
                margin: 10px;
                padding: 15px;
            }
        """)
        
        nav_layout = QHBoxLayout(nav_frame)
        
        # Previous button
        self.prev_btn = QPushButton('← Previous')
        self.prev_btn.setFixedHeight(50)
        self.prev_btn.clicked.connect(self.previous_page)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover:enabled {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        nav_layout.addWidget(self.prev_btn)
        
        # Page info
        self.page_label = QLabel('Page 1 of 1')
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding: 12px 20px;
            }
        """)
        nav_layout.addWidget(self.page_label, 1)
        
        # Next button
        self.next_btn = QPushButton('Next →')
        self.next_btn.setFixedHeight(50)
        self.next_btn.clicked.connect(self.next_page)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover:enabled {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        nav_layout.addWidget(self.next_btn)
        
        parent_layout.addWidget(nav_frame)

    def update_grid_display(self):
        """Update the grid display with current plants"""
        # Clear existing grid
        for i in reversed(range(self.grid_layout.count())):
            child = self.grid_layout.itemAt(i)
            if child and child.widget():
                child.widget().deleteLater()
        
        # Update stats
        start_idx = self.current_page * self.plants_per_page + 1
        end_idx = min(start_idx + len(self.current_plants) - 1, self.total_plants)
        self.stats_label.setText(
            f'Showing {start_idx}-{end_idx} of {self.total_plants} plants'
        )
        
        # Add plant cards in 3x3 grid
        if not self.current_plants:
            no_results = QLabel('No plants found matching your criteria.')
            no_results.setAlignment(Qt.AlignCenter)
            no_results.setStyleSheet("""
                QLabel {
                    font-size: 20px;
                    color: #666;
                    padding: 50px;
                    background-color: white;
                    border-radius: 12px;
                    border: 3px solid #e0e0e0;
                }
            """)
            self.grid_layout.addWidget(no_results, 0, 0, 1, 3)
        else:
            row = 0
            col = 0
            for plant_data in self.current_plants:
                plant_card = PlantCard(plant_data)
                plant_card.clicked.connect(self.show_plant_detail)
                self.grid_layout.addWidget(plant_card, row, col)
                
                col += 1
                if col >= 3:  # 3 cards per row for touch interface
                    col = 0
                    row += 1
        
        # Update navigation
        self.update_navigation()

    def show_plant_detail(self, plant_data):
        """Show detailed view for a plant"""
        self.detail_view.show_plant(plant_data)
        self.stack.setCurrentWidget(self.detail_view)

    def show_grid_view(self):
        """Return to grid view"""
        self.stack.setCurrentWidget(self.grid_page)

    def on_search_changed(self):
        """Handle search text changes with debounce"""
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
            
            self.update_grid_display()
            
        except Exception as e:
            QMessageBox.critical(self, 'Database Error', f'Failed to load plants:\n{str(e)}')

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