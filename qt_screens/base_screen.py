"""
Base screen class for PySide6 screens with common functionality
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

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
        },
        'text': {
            'secondary': '#333333'
        }
    }

class BaseScreen(QWidget):
    """Base class for all application screens with common UI elements"""
    
    def __init__(self, db_manager, main_window):
        super().__init__()
        self.db_manager = db_manager
        self.main_window = main_window
        
        # Initialize UI
        self.init_base_ui()
        self.build_ui()
        
    def init_base_ui(self):
        """Initialize common UI elements"""
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)
        
    def build_ui(self):
        """Override this method to build screen-specific UI"""
        pass
        
    def create_button(self, text, callback, style_class='default'):
        """Create a styled button with consistent appearance"""
        button = QPushButton(text)
        
        # Set button font size
        font = button.font()
        font.setPointSize(14)
        button.setFont(font)
        
        # Set minimum height for touch interface
        button.setMinimumHeight(65)  # Touch-friendly height
        
        # Apply styling with design system colors - optimized for touch
        if style_class == 'primary':
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {APP_COLORS['core']['blue_gray']};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {APP_COLORS['blue_gray_family']['dark']};
                }}
                QPushButton:pressed {{
                    background-color: {APP_COLORS['blue_gray_family']['darker']};
                }}
            """)
        elif style_class == 'secondary':
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {APP_COLORS['core']['teal_gray']};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {APP_COLORS['teal_gray_family']['dark']};
                }}
                QPushButton:pressed {{
                    background-color: {APP_COLORS['teal_gray_family']['darker']};
                }}
            """)
        elif style_class == 'warning':
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {APP_COLORS['core']['purple_gray']};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {APP_COLORS['purple_gray_family']['dark']};
                }}
                QPushButton:pressed {{
                    background-color: {APP_COLORS['purple_gray_family']['darker']};
                }}
            """)
        elif style_class == 'danger':
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {APP_COLORS['extended']['error']};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #c82333;
                }}
                QPushButton:pressed {{
                    background-color: #a71e2a;
                }}
            """)
        else:  # default
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {APP_COLORS['text']['secondary']};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {APP_COLORS['text']['muted']};
                }}
                QPushButton:pressed {{
                    background-color: {APP_COLORS['blue_gray_family']['darker']};
                }}
            """)
        
        # Connect callback
        button.clicked.connect(callback)
        
        return button
        
    def create_header(self, title, show_back_button=True):
        """Create a standard header with title and optional back button"""
        header_layout = QHBoxLayout()
        
        if show_back_button:
            # Import here to avoid circular import
            from .icon_manager import create_icon_button
            back_button = create_icon_button("back", "Back", (24, 24), self.go_back)
            back_button.setMaximumWidth(120)
            back_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {APP_COLORS['text']['secondary']};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                    text-align: left;
                    padding-left: 18px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {APP_COLORS['text']['muted']};
                }}
                QPushButton:pressed {{
                    background-color: {APP_COLORS['blue_gray_family']['darker']};
                }}
            """)
            header_layout.addWidget(back_button)
            
        # Title label
        title_label = QLabel(title)
        title_font = title_label.font()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {APP_COLORS['core']['blue_gray']}; margin: 10px;")
        
        if show_back_button:
            header_layout.addWidget(title_label, 1)
            header_layout.addWidget(QLabel(""), 0)  # Spacer for balance
        else:
            header_layout.addWidget(title_label, 1, Qt.AlignCenter)
            
        return header_layout
        
    def create_title_label(self, text, size='large'):
        """Create a styled title label"""
        label = QLabel(text)
        font = label.font()
        
        if size == 'large':
            font.setPointSize(20)
        elif size == 'medium':
            font.setPointSize(16)
        else:  # small
            font.setPointSize(12)
            
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"color: {APP_COLORS['core']['blue_gray']}; margin: 10px;")
        
        return label
        
    def go_back(self):
        """Navigate back to home screen"""
        self.main_window.show_screen('home')
        
    def go_to_screen(self, screen_name):
        """Navigate to a specific screen"""
        self.main_window.show_screen(screen_name)
        
    def on_enter(self):
        """Called when screen becomes active - override in subclasses"""
        pass