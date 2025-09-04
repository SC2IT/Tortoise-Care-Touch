"""
Plant Database Screen - Modern Grid Layout with Touch Interface
Browse and search plant database with large photos and detailed views
"""

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                              QLabel, QLineEdit, QScrollArea, QWidget, QMessageBox,
                              QComboBox, QFrame, QStackedWidget, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap
from .base_screen import BaseScreen
from .icon_manager import create_icon_button

# Centralized color scheme for consistency
PLANT_COLORS = {
    # Header badge colors for detail view
    'header_badges': {
        'safe': {'bg': '#28a745', 'text': '#ffffff'},
        'caution': {'bg': '#ffc107', 'text': '#333333'},
        'toxic': {'bg': '#dc3545', 'text': '#ffffff'}
    },
    # Info box background colors for detail view
    'info_backgrounds': {
        'safe': {'bg': '#e6f4e6', 'text': '#000000'},
        'caution': {'bg': '#fff8dc', 'text': '#000000'},
        'toxic': {'bg': '#ffe6e6', 'text': '#000000'}
    },
    # Tile badge colors (keep original strong colors for visibility)
    'tile_badges': {
        'safe': {'bg': '#28a745', 'shadow': 'rgba(40, 167, 69, 0.2)'},
        'caution': {'bg': '#ffc107', 'shadow': 'rgba(255, 193, 7, 0.2)'},
        'toxic': {'bg': '#dc3545', 'shadow': 'rgba(220, 53, 69, 0.2)'}
    }
}

class PlantCard(QFrame):
    """Individual plant card widget for grid display"""
    clicked = Signal(tuple)
    
    def __init__(self, plant_data):
        super().__init__()
        self.plant_data = plant_data
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the plant card UI - Authentic Tortoise Table photo-focused design"""
        # Current database format has 7 values (with photo)
        name, sci_name, safety_level, nutrition_notes, frequency, description, photo_path = self.plant_data
        
        # Use centralized colors
        color = PLANT_COLORS['tile_badges'].get(safety_level, PLANT_COLORS['tile_badges']['safe'])
        
        # Card size reduced to prevent scrolling
        self.setFixedSize(200, 340)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {color['bg']};
                border-radius: 8px;
                margin: 4px;
            }}
            QFrame:hover {{
                border: 1px solid {color['bg']};
                background-color: #f8f9fa;
            }}
        """)
        
        # Use absolute positioning for centered layout
        self.setLayout(None)
        
        # Photo area - at the top
        self.photo_label = QLabel(self)
        self.photo_label.setGeometry(10, 10, 180, 180)  # Back at the top
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("""
            QLabel {
                border-radius: 8px;
                background-color: #f8f9fa;
            }
        """)
        
        # Load photo or show placeholder
        if photo_path:
            try:
                from pathlib import Path
                photo_file = Path(photo_path)
                if photo_file.exists():
                    pixmap = QPixmap(str(photo_file))
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.photo_label.setPixmap(scaled_pixmap)
                    else:
                        self.set_grid_placeholder(self.photo_label, name)
                else:
                    self.set_grid_placeholder(self.photo_label, name)
            except Exception:
                self.set_grid_placeholder(self.photo_label, name)
        else:
            self.set_grid_placeholder(self.photo_label, name)
        
        # Plant name - 3px gap from photo, truncate if too long
        # Truncate plant name if longer than ~15 characters
        display_name = name if len(name) <= 15 else name[:12] + "..."
        self.name_label = QLabel(display_name, self)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setGeometry(10, 193, 180, 40)
        self.name_label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.95);
                color: #000;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                border-radius: 6px;
            }
        """)
        
        # Scientific name - 3px gap from plant name, truncate if too long
        # Truncate scientific name if longer than ~25 characters  
        display_sci_name = sci_name if len(sci_name) <= 25 else sci_name[:22] + "..."
        self.sci_label = QLabel(display_sci_name, self)
        self.sci_label.setAlignment(Qt.AlignCenter)
        self.sci_label.setWordWrap(True) 
        self.sci_label.setGeometry(10, 236, 180, 50)
        self.sci_label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.9);
                color: #333;
                font-size: 14px;
                font-style: italic;
                padding: 8px;
                border-radius: 6px;
                line-height: 1.3;
            }
        """)
        
        # Safety indicator - 3px gap from scientific name
        safety_text = {
            'safe': '✓ Safe',
            'caution': '⚠ Caution', 
            'toxic': '✗ Toxic'
        }.get(safety_level, 'Unknown')
        
        self.safety_label = QLabel(safety_text, self)
        self.safety_label.setAlignment(Qt.AlignCenter)
        self.safety_label.setGeometry(10, 289, 180, 40)
        self.safety_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color['bg']};
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 8px;
                border-radius: 6px;
            }}
        """)
        
        # Bring all text labels to front layer
        self.name_label.raise_()
        self.sci_label.raise_()
        self.safety_label.raise_()
        
    def set_grid_placeholder(self, label, plant_name):
        """Set placeholder for grid cards"""
        label.setText(f"🌿\n{plant_name}\nNo photo")
        label.setStyleSheet("""
            QLabel {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: #f8f9fa;
                color: #6c757d;
                font-size: 10px;
                font-weight: 500;
            }
        """)
        
    def mousePressEvent(self, event):
        """Handle card click - go to detail view"""
        if event.button() == Qt.LeftButton:
            if self.plant_data:
                self.clicked.emit(self.plant_data)
        super().mousePressEvent(event)

class PlantDetailView(QWidget):
    """Detailed view for individual plant - Tortoise Table style"""
    back_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_plant_data = None
        self.main_window = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Setup fullscreen overlay detail view"""
        # Make this widget a fullscreen overlay like the photo viewer
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(1280, 720)
        
        # Initially hidden - will be shown when needed
        self.hide()
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Content widget that fills entire screen
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
            }
        """)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        main_layout.addWidget(self.content_widget)
        
    def show_plant(self, plant_data):
        """Display plant in Tortoise Table style"""
        # Clear existing content
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        # Store plant data for fullscreen viewer
        self.current_plant_data = plant_data
        
        # Validate plant_data - expect exactly 7 values
        if not plant_data or len(plant_data) != 7:
            error_label = QLabel("Error: Invalid plant data")
            error_label.setStyleSheet("font-size: 18px; color: red; padding: 20px;")
            self.content_layout.addWidget(error_label)
            return
                
        # Current database format has 7 values (with photo)
        name, sci_name, safety_level, nutrition_notes, frequency, description, photo_path = plant_data
        
        # Main fullscreen container with integrated header
        main_container = QWidget()
        main_container.setStyleSheet("background-color: #f5f5f5;")
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top section with back button and plant title - integrated into fullscreen view
        top_section = QWidget()
        top_section.setFixedHeight(80)
        # Complementary header colors based on safety level
        header_colors = {
            'safe': '#5a7a8a',      # Blue-gray - contrasts well with green badge
            'caution': '#6b5a8a',   # Purple-gray - contrasts well with yellow badge
            'toxic': '#5a8a7a'      # Teal-gray - contrasts well with red badge
        }
        header_color = header_colors.get(safety_level.lower(), '#9cafb7')  # Default blue-gray
        
        top_section.setStyleSheet(f"""
            QWidget {{
                background-color: {header_color};
            }}
        """)
        
        top_layout = QHBoxLayout(top_section)
        top_layout.setContentsMargins(20, 15, 20, 15)
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedHeight(50)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 8px 20px;
                font-size: 18px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        back_btn.clicked.connect(self.close_detail_view)
        top_layout.addWidget(back_btn)
        
        # Plant title in the fullscreen header (just name, not scientific name)
        plant_title = QLabel(name)
        plant_title.setAlignment(Qt.AlignCenter)
        plant_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
                margin: 0px 20px;
            }
        """)
        top_layout.addWidget(plant_title, 1)
        
        # Safety badge in header right corner
        safety_badge_header = QLabel(safety_level.upper())
        safety_badge_header.setFixedHeight(50)
        safety_badge_header.setAlignment(Qt.AlignCenter)
        # Use centralized header badge colors
        style = PLANT_COLORS['header_badges'].get(safety_level.lower(), PLANT_COLORS['header_badges']['safe'])
        safety_badge_header.setStyleSheet(f"""
            QLabel {{
                color: {style['text']};
                background-color: {style['bg']};
                font-size: 18px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 15px;
                margin-right: 10px;
            }}
        """)
        top_layout.addWidget(safety_badge_header)
        
        main_layout.addWidget(top_section)
        
        # Main content area - reduced height to make room for photos at bottom
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #f5f5f5;")
        content_layout_main = QVBoxLayout(content_area)
        content_layout_main.setContentsMargins(10, 10, 10, 10)
        content_layout_main.setSpacing(10)
        
        # Horizontal layout for photo, info, and map - scaled to fit 1240px width
        content_horizontal = QWidget()
        content_layout = QHBoxLayout(content_horizontal)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left - Main photo section (resized for exact 10px spacing)
        photo_widget = QWidget()
        photo_widget.setFixedSize(490, 500)  # Increased height to fill space
        photo_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
            }
        """)
        
        photo_layout = QVBoxLayout(photo_widget)
        photo_layout.setContentsMargins(5, 5, 5, 5)
        photo_layout.setSpacing(0)
        
        # Main photo - landscape orientation
        self.main_photo_label = QLabel()
        self.main_photo_label.setFixedSize(480, 490)  # Increased height to fill space
        self.main_photo_label.setAlignment(Qt.AlignCenter)
        self.main_photo_label.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: #f8f9fa;
            }
        """)
        
        # Make photo clickable for fullscreen
        self.main_photo_label.mousePressEvent = self.on_photo_clicked
        
        # Load photo or placeholder
        if photo_path:
            try:
                from pathlib import Path
                photo_file = Path(photo_path)
                if photo_file.exists():
                    pixmap = QPixmap(str(photo_file))
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(488, 508, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.main_photo_label.setPixmap(scaled_pixmap)
                    else:
                        self.main_photo_label.setText(f"🌱\n\nNo Photo Available\nfor {name}")
                        self.main_photo_label.setStyleSheet(self.main_photo_label.styleSheet() + "color: #999; font-size: 20px;")
                else:
                    self.main_photo_label.setText(f"🌱\n\nNo Photo Available\nfor {name}")
                    self.main_photo_label.setStyleSheet(self.main_photo_label.styleSheet() + "color: #999; font-size: 20px;")
            except:
                self.main_photo_label.setText(f"🌱\n\nNo Photo Available\nfor {name}")
                self.main_photo_label.setStyleSheet(self.main_photo_label.styleSheet() + "color: #999; font-size: 20px;")
        else:
            self.main_photo_label.setText(f"🌱\n\nNo Photo Available\nfor {name}")
            self.main_photo_label.setStyleSheet(self.main_photo_label.styleSheet() + "color: #999; font-size: 20px;")
        
        photo_layout.addWidget(self.main_photo_label)
        content_layout.addWidget(photo_widget)
        
        # Middle - Plant information (resized for exact 10px spacing)
        info_widget = QWidget()
        info_widget.setFixedSize(586, 500)
        
        # Use centralized info box colors
        box_style = PLANT_COLORS['info_backgrounds'].get(safety_level.lower(), PLANT_COLORS['info_backgrounds']['safe'])
        
        info_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {box_style['bg']};
                border-radius: 12px;
                color: {box_style['text']};
            }}
        """)
        
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(10, 10, 10, 10)
        info_layout.setSpacing(10)
        
        # Safety badge moved to header - this section removed
        
        # Scientific name - compact sizing for single line
        sci_name_label = QLabel(sci_name or "Scientific name not available")
        sci_name_label.setWordWrap(True)
        sci_name_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-style: italic;
                background-color: rgba(255, 255, 255, 0.8);
                padding: 6px 8px;
                border-radius: 6px;
            }
        """)
        sci_name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        info_layout.addWidget(sci_name_label, 0)  # No stretch factor - minimum space
        
        # Description - takes up more space proportionally
        desc_label = QLabel(description or "No description available")
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                line-height: 1.5;
                background-color: rgba(255, 255, 255, 0.8);
                padding: 10px;
                border-radius: 8px;
            }
        """)
        desc_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        info_layout.addWidget(desc_label, 2)  # Gets 2x the space
        
        # Nutrition notes - medium space
        nutrition_label = QLabel(f"Nutrition: {nutrition_notes or 'No nutrition information available'}")
        nutrition_label.setWordWrap(True)
        nutrition_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                background-color: rgba(255, 255, 255, 0.8);
                padding: 10px;
                border-radius: 8px;
            }
        """)
        nutrition_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        info_layout.addWidget(nutrition_label, 1)  # Gets 1x the space
        
        # Feeding frequency - compact for typically short text
        frequency_label = QLabel(f"Feeding: {frequency or 'Feeding frequency not specified'}")
        frequency_label.setWordWrap(True)
        frequency_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                background-color: rgba(255, 255, 255, 0.8);
                padding: 10px;
                border-radius: 8px;
            }
        """)
        frequency_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        info_layout.addWidget(frequency_label, 0)  # No stretch - minimum space
        
        content_layout.addWidget(info_widget)
        
        # Right - Map area (resized for exact 10px spacing)
        map_widget = QWidget()
        map_widget.setFixedSize(164, 500)
        map_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
            }
        """)
        
        map_layout = QVBoxLayout(map_widget)
        map_layout.setContentsMargins(10, 10, 10, 10)
        
        # Map title
        map_title = QLabel("Local\nOccurrence")
        map_title.setAlignment(Qt.AlignCenter)
        map_title.setWordWrap(True)
        map_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding: 10px 4px;
            }
        """)
        map_layout.addWidget(map_title)
        
        # Map placeholder
        map_placeholder = QLabel("🗺️\n\nMap data\ncoming soon")
        map_placeholder.setAlignment(Qt.AlignCenter)
        map_placeholder.setWordWrap(True)
        map_placeholder.setStyleSheet("""
            QLabel {
                color: #999;
                font-size: 14px;
                background-color: #f8f9fa;
                border: 1px dashed #ddd;
                border-radius: 6px;
                padding: 10px;
                margin: 5px 0px;
            }
        """)
        map_layout.addWidget(map_placeholder)
        
        # "Click for map" button
        map_button = QLabel("click for map")
        map_button.setAlignment(Qt.AlignCenter)
        map_button.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-size: 15px;
                font-style: italic;
                text-decoration: underline;
            }
        """)
        map_layout.addWidget(map_button)
        
        content_layout.addWidget(map_widget)
        content_layout_main.addWidget(content_horizontal)
        
        main_layout.addWidget(content_area)
        
        # Bottom photo strip - spans entire width with thumbnails
        photo_strip = QWidget()
        photo_strip.setFixedHeight(100)
        photo_strip.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border-top: 1px solid #ddd;
            }
        """)
        
        photo_strip_layout = QHBoxLayout(photo_strip)
        photo_strip_layout.setContentsMargins(5, 5, 5, 5)
        photo_strip_layout.setSpacing(3)  # Tiny padding between thumbnails
        
        # Sample thumbnails (placeholder for future multiple photos)
        for i in range(8):  # Show 8 thumbnail placeholders
            thumbnail = QLabel(f"Img\n{i+1}")
            thumbnail.setFixedSize(90, 90)
            thumbnail.setAlignment(Qt.AlignCenter)
            thumbnail.setStyleSheet("""
                QLabel {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-size: 12px;
                    color: #999;
                }
                QLabel:hover {
                    border: 2px solid #28a745;
                }
            """)
            photo_strip_layout.addWidget(thumbnail)
        
        photo_strip_layout.addStretch()  # Push thumbnails to left
        
        main_layout.addWidget(photo_strip)
        
        self.content_layout.addWidget(main_container)
        
        # Position overlay exactly over the main window
        if self.main_window:
            main_pos = self.main_window.pos()
            self.move(main_pos)
        
        # Show the fullscreen overlay
        self.show()
        self.raise_()  # Bring to front
        self.activateWindow()  # Make sure it's active
    
    def close_detail_view(self):
        """Close the detail view overlay and emit back signal"""
        self.hide()
        self.back_clicked.emit()
    
    def on_photo_clicked(self, event):
        """Handle photo click to show fullscreen viewer"""
        if self.current_plant_data and event.button() == Qt.LeftButton:
            # Create and show fullscreen viewer
            fullscreen_viewer = FullscreenPhotoViewer(self.current_plant_data, self)
            fullscreen_viewer.showFullScreen()

class FullscreenPhotoViewer(QWidget):
    """Fullscreen photo viewer with touch controls"""
    closed = Signal()
    
    def __init__(self, plant_data, parent=None):
        super().__init__(parent)
        self.plant_data = plant_data
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Get plant info
        name, sci_name, safety_level, nutrition_notes, frequency, description, photo_path = plant_data
        
        self.setup_ui(name, photo_path)
        
    def setup_ui(self, plant_name, photo_path):
        """Setup fullscreen photo viewer UI"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Semi-transparent black background
        background = QWidget()
        background.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.9);
            }
        """)
        
        bg_layout = QVBoxLayout(background)
        bg_layout.setContentsMargins(20, 20, 20, 20)
        bg_layout.setSpacing(0)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(50, 50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 25px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        close_btn.clicked.connect(self.close_viewer)
        
        # Top bar with close button
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(close_btn)
        bg_layout.addLayout(top_bar)
        
        # Photo area
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setMinimumSize(200, 200)
        
        # Load photo
        if photo_path:
            try:
                from pathlib import Path
                photo_file = Path(photo_path)
                if photo_file.exists():
                    pixmap = QPixmap(str(photo_file))
                    if not pixmap.isNull():
                        # Scale to fit screen while maintaining aspect ratio
                        screen_size = self.screen().availableGeometry().size()
                        max_width = screen_size.width() - 100
                        max_height = screen_size.height() - 200
                        
                        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.photo_label.setPixmap(scaled_pixmap)
                    else:
                        self.set_fullscreen_placeholder(plant_name)
                else:
                    self.set_fullscreen_placeholder(plant_name)
            except Exception:
                self.set_fullscreen_placeholder(plant_name)
        else:
            self.set_fullscreen_placeholder(plant_name)
        
        bg_layout.addWidget(self.photo_label)
        
        # Plant name at bottom
        name_label = QLabel(plant_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: 600;
                padding: 20px;
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 8px;
            }
        """)
        bg_layout.addWidget(name_label)
        
        layout.addWidget(background)
        
    def set_fullscreen_placeholder(self, plant_name):
        """Set fullscreen placeholder"""
        self.photo_label.setText(f"🌿\n\n{plant_name}\n\nNo photo available")
        self.photo_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px dashed rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                padding: 50px;
            }
        """)
    
    def mousePressEvent(self, event):
        """Close on background click"""
        if event.button() == Qt.LeftButton:
            self.close_viewer()
    
    def keyPressEvent(self, event):
        """Close on Escape key"""
        if event.key() == Qt.Key.Key_Escape:
            self.close_viewer()
        super().keyPressEvent(event)
    
    def close_viewer(self):
        """Close the fullscreen viewer"""
        self.closed.emit()
        self.close()

class PlantDatabaseScreen(BaseScreen):
    """Plant database with modern grid layout and touch interface"""
    
    def __init__(self, db_manager, main_window):
        # Initialize attributes before calling parent __init__
        self.current_plants = []
        self.plants_per_page = 12  # 4x3 grid for touch interface
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
        
        # Detail view - now a fullscreen overlay, not added to stack
        # Pass parent to properly position the overlay
        self.detail_view = PlantDetailView(self.parent())
        self.detail_view.back_clicked.connect(self.show_grid_view)
        
        # Start with grid view
        self.stack.setCurrentWidget(self.grid_page)
        
        # Load initial data
        self.load_plants()
        
    def setup_grid_view(self):
        """Setup the grid view layout"""
        layout = QVBoxLayout(self.grid_page)
        layout.setSpacing(5)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Search and filter section
        self.create_search_section(layout)
        
        
        # Grid content area - expanded to fill available space
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
                margin: 5px;
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
                border: 3px solid #e0e0e0;
                border-radius: 12px;
                background-color: #f8f8f8;
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
        
        # Grid layout for plant cards (4 columns)
        self.grid_layout = QGridLayout(self.content_widget)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)  # Reduced margins to prevent unnecessary scrolling
        
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
                margin: 5px;
                padding: 8px 15px;
            }
        """)
        
        nav_layout = QHBoxLayout(nav_frame)
        
        # Previous button
        self.prev_btn = QPushButton('← Previous')
        self.prev_btn.setFixedHeight(40)
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
                font-size: 14px;
                font-weight: bold;
                color: #333;
                padding: 8px 16px;
            }
        """)
        nav_layout.addWidget(self.page_label, 1)
        
        # Next button
        self.next_btn = QPushButton('Next →')
        self.next_btn.setFixedHeight(40)
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
        
        # Remove the separate stats display since it's now in pagination
        
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
            self.grid_layout.addWidget(no_results, 0, 0, 1, 4)
        else:
            row = 0
            col = 0
            for plant_data in self.current_plants:
                # plant_data is already a tuple from the database query
                plant_card = PlantCard(plant_data)
                plant_card.clicked.connect(self.show_plant_detail)
                self.grid_layout.addWidget(plant_card, row, col)
                
                col += 1
                if col >= 4:  # 4 cards per row for touch interface
                    col = 0
                    row += 1
        
        # Update navigation
        self.update_navigation()

    def show_plant_detail(self, plant_data):
        """Show detailed view for a plant as fullscreen overlay"""
        if plant_data and len(plant_data) == 7:
            self.detail_view.show_plant(plant_data)
            # No need to change stack - detail view is now a fullscreen overlay
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", f"Invalid plant data received")

    def show_fullscreen_photo(self, plant_data):
        """Show fullscreen photo viewer"""
        if plant_data and len(plant_data) == 7:
            self.fullscreen_viewer = FullscreenPhotoViewer(plant_data, self)
            self.fullscreen_viewer.closed.connect(self.on_fullscreen_closed)
            self.fullscreen_viewer.showFullScreen()
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", f"Invalid plant data received")
    
    def on_fullscreen_closed(self):
        """Handle fullscreen viewer closing"""
        if hasattr(self, 'fullscreen_viewer'):
            self.fullscreen_viewer.deleteLater()
            del self.fullscreen_viewer

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
            raw_plants = cursor.fetchall()
            
            # Convert sqlite3.Row objects to tuples immediately
            self.current_plants = [tuple(plant) for plant in raw_plants]
            
            
            self.update_grid_display()
            
        except Exception as e:
            QMessageBox.critical(self, 'Database Error', f'Failed to load plants:\n{str(e)}')

    def update_navigation(self):
        """Update pagination controls"""
        total_pages = max(1, (self.total_plants + self.plants_per_page - 1) // self.plants_per_page)
        current_page_display = self.current_page + 1
        
        # Calculate display range
        start_idx = self.current_page * self.plants_per_page + 1
        end_idx = min(start_idx + len(self.current_plants) - 1, self.total_plants)
        
        self.page_label.setText(f'Page {current_page_display} of {total_pages} • Showing {start_idx}-{end_idx} of {self.total_plants}')
        
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