from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger

class OrientationManager(EventDispatcher):
    """
    Manages screen orientation detection and UI adaptation for Pi Touch Display 2
    Supports both 720x1280 (portrait) and 1280x720 (landscape) orientations
    """
    
    __events__ = ('on_orientation_change',)
    
    def __init__(self):
        super().__init__()
        self.current_orientation = self._detect_orientation()
        self.previous_orientation = self.current_orientation
        
        # Bind to window size changes
        Window.bind(size=self._on_window_resize)
        
        # Schedule periodic orientation checks (in case hardware rotation happens)
        Clock.schedule_interval(self._check_orientation, 0.5)
        
        Logger.info(f"OrientationManager: Initial orientation: {self.current_orientation}")
    
    def _detect_orientation(self):
        """Detect current orientation based on window dimensions"""
        width, height = Window.size
        
        # Pi Touch Display 2 native resolutions
        if width == 720 and height == 1280:
            return 'portrait'
        elif width == 1280 and height == 720:
            return 'landscape'
        else:
            # Fallback: determine by aspect ratio
            if width > height:
                return 'landscape'
            else:
                return 'portrait'
    
    def _on_window_resize(self, window, width, height):
        """Handle window resize events"""
        new_orientation = self._detect_orientation()
        
        if new_orientation != self.current_orientation:
            Logger.info(f"OrientationManager: Window resize detected - {self.current_orientation} -> {new_orientation}")
            self._update_orientation(new_orientation)
    
    def _check_orientation(self, dt):
        """Periodic check for orientation changes"""
        new_orientation = self._detect_orientation()
        
        if new_orientation != self.current_orientation:
            Logger.info(f"OrientationManager: Orientation change detected - {self.current_orientation} -> {new_orientation}")
            self._update_orientation(new_orientation)
    
    def _update_orientation(self, new_orientation):
        """Update orientation and notify listeners"""
        self.previous_orientation = self.current_orientation
        self.current_orientation = new_orientation
        
        # Dispatch orientation change event
        self.dispatch('on_orientation_change', new_orientation, self.previous_orientation)
    
    def on_orientation_change(self, new_orientation, previous_orientation):
        """Default event handler - override in subclasses"""
        pass
    
    def is_portrait(self):
        """Check if current orientation is portrait"""
        return self.current_orientation == 'portrait'
    
    def is_landscape(self):
        """Check if current orientation is landscape"""
        return self.current_orientation == 'landscape'
    
    def get_layout_config(self):
        """Get layout configuration for current orientation"""
        if self.is_portrait():
            return {
                'nav_columns': 1,      # Single column for portrait
                'input_columns': 2,    # 2 columns for input forms
                'input_rows': 2,       # 2 rows for input forms
                'button_spacing': 15,  # More vertical spacing
                'font_size_large': '20sp',
                'font_size_medium': '16sp',
                'font_size_small': '14sp',
                'header_height': 0.08,
                'button_height': 60,
                'input_height': 50
            }
        else:  # landscape
            return {
                'nav_columns': 2,      # Two columns for landscape
                'input_columns': 4,    # 4 columns for input forms
                'input_rows': 1,       # 1 row for input forms
                'button_spacing': 20,  # More horizontal spacing
                'font_size_large': '18sp',
                'font_size_medium': '14sp',
                'font_size_small': '12sp',
                'header_height': 0.12,
                'button_height': 50,
                'input_height': 45
            }
    
    def force_orientation_check(self):
        """Force an immediate orientation check"""
        self._check_orientation(0)
    
    def get_window_info(self):
        """Get current window information for debugging"""
        return {
            'size': Window.size,
            'orientation': self.current_orientation,
            'width': Window.width,
            'height': Window.height
        }