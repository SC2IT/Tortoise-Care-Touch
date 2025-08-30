from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
from utils.orientation_manager import OrientationManager

class BaseScreen(Screen):
    """
    Base screen class with orientation awareness
    All other screens should inherit from this class
    """
    
    def __init__(self, db_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.db_manager = db_manager
        self.orientation_manager = None
        self.layout_config = None
        self.is_built = False
    
    def set_orientation_manager(self, orientation_manager):
        """Set the orientation manager and bind to events"""
        self.orientation_manager = orientation_manager
        self.layout_config = orientation_manager.get_layout_config()
        
        # Bind to orientation changes
        self.orientation_manager.bind(on_orientation_change=self.on_orientation_change)
        
        # Initial build if not done yet
        if not self.is_built:
            self.build_ui()
            self.is_built = True
    
    def on_orientation_change(self, manager, new_orientation, previous_orientation):
        """Handle orientation changes by rebuilding UI"""
        Logger.info(f"{self.__class__.__name__}: Orientation changed to {new_orientation}")
        
        # Update layout config
        self.layout_config = self.orientation_manager.get_layout_config()
        
        # Rebuild UI with new orientation
        self.clear_widgets()
        self.build_ui()
        
        # Call custom orientation change handler if implemented
        if hasattr(self, 'handle_orientation_change'):
            self.handle_orientation_change(new_orientation, previous_orientation)
    
    def build_ui(self):
        """
        Build the UI - should be implemented by subclasses
        Use self.layout_config for orientation-aware layout
        """
        raise NotImplementedError("Subclasses must implement build_ui()")
    
    def get_nav_columns(self):
        """Get number of navigation columns for current orientation"""
        return self.layout_config['nav_columns'] if self.layout_config else 1
    
    def get_input_columns(self):
        """Get number of input columns for current orientation"""
        return self.layout_config['input_columns'] if self.layout_config else 2
    
    def get_input_rows(self):
        """Get number of input rows for current orientation"""
        return self.layout_config['input_rows'] if self.layout_config else 2
    
    def get_button_spacing(self):
        """Get button spacing for current orientation"""
        return self.layout_config['button_spacing'] if self.layout_config else 15
    
    def get_font_size(self, size_type='medium'):
        """Get font size for current orientation"""
        if not self.layout_config:
            return '16sp'
        
        size_map = {
            'large': self.layout_config['font_size_large'],
            'medium': self.layout_config['font_size_medium'], 
            'small': self.layout_config['font_size_small']
        }
        
        return size_map.get(size_type, '16sp')
    
    def get_header_height(self):
        """Get header height ratio for current orientation"""
        return self.layout_config['header_height'] if self.layout_config else 0.08
    
    def get_button_height(self):
        """Get button height for current orientation"""
        return self.layout_config['button_height'] if self.layout_config else 60
    
    def get_input_height(self):
        """Get input field height for current orientation"""
        return self.layout_config['input_height'] if self.layout_config else 50
    
    def is_portrait(self):
        """Check if current orientation is portrait"""
        return self.orientation_manager.is_portrait() if self.orientation_manager else True
    
    def is_landscape(self):
        """Check if current orientation is landscape"""
        return self.orientation_manager.is_landscape() if self.orientation_manager else False