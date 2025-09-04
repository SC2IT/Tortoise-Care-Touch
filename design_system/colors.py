"""
Tortoise Care Touch - Comprehensive Color Theory Palette
Based on the sophisticated plant safety color scheme with full color relationships
"""

# Complete color theory palette based on our three main colors
APP_COLORS = {
    # Core triadic colors (our main colors)
    'core': {
        'blue_gray': '#5a7a8a',     # Primary (safe plant complement)
        'purple_gray': '#6b5a8a',   # Secondary (caution plant complement) 
        'teal_gray': '#5a8a7a',     # Tertiary (toxic plant complement)
    },
    
    # Monochromatic variations of each core color
    'blue_gray_family': {
        'lightest': '#e8edf0',      # Very light blue-gray
        'lighter': '#d1dae1',       # Light blue-gray
        'light': '#a3b5c2',         # Medium-light blue-gray
        'base': '#5a7a8a',          # Base blue-gray (our main color)
        'dark': '#4a6673',          # Dark blue-gray
        'darker': '#3a525c',        # Darker blue-gray
        'darkest': '#2a3e45',       # Very dark blue-gray
    },
    
    'purple_gray_family': {
        'lightest': '#eee8f0',      # Very light purple-gray
        'lighter': '#ddd1e1',       # Light purple-gray
        'light': '#b5a3c2',         # Medium-light purple-gray
        'base': '#6b5a8a',          # Base purple-gray (our main color)
        'dark': '#5a4a73',          # Dark purple-gray
        'darker': '#493a5c',        # Darker purple-gray
        'darkest': '#382a45',       # Very dark purple-gray
    },
    
    'teal_gray_family': {
        'lightest': '#e8f0ed',      # Very light teal-gray
        'lighter': '#d1e1da',       # Light teal-gray
        'light': '#a3c2b5',         # Medium-light teal-gray
        'base': '#5a8a7a',          # Base teal-gray (our main color)
        'dark': '#4a7366',          # Dark teal-gray
        'darker': '#3a5c52',        # Darker teal-gray
        'darkest': '#2a453e',       # Very dark teal-gray
    },
    
    # Analogous colors (neighbors on color wheel)
    'analogous': {
        'blue_neighbors': ['#5a7a9a', '#5a6a8a', '#5a8a9a'],      # Blue variations
        'purple_neighbors': ['#7a5a8a', '#6a5a8a', '#8a5a9a'],    # Purple variations  
        'teal_neighbors': ['#5a9a8a', '#5a8a6a', '#6a8a5a'],      # Teal variations
    },
    
    # Complementary colors (opposite on color wheel)
    'complementary': {
        'blue_gray_complement': '#8a6a5a',    # Warm brown (opposite of blue-gray)
        'purple_gray_complement': '#5a8a6a',  # Warm green (opposite of purple-gray)
        'teal_gray_complement': '#8a5a6a',    # Warm magenta (opposite of teal-gray)
    },
    
    # Split complementary (more sophisticated than direct complements)
    'split_complementary': {
        'blue_gray_splits': ['#8a5a6a', '#8a7a5a'],     # Magenta + Orange
        'purple_gray_splits': ['#6a8a5a', '#5a8a7a'],   # Green + Teal
        'teal_gray_splits': ['#6a5a8a', '#8a6a5a'],     # Purple + Orange
    },
    
    # Triadic harmony (equidistant on color wheel)
    'triadic': {
        'primary_triad': ['#5a7a8a', '#8a5a7a', '#7a8a5a'],      # Our main triad
        'secondary_triad': ['#6b5a8a', '#8a6b5a', '#5a8a6b'],    # Secondary triad
    },
    
    # Light background colors for content areas
    'backgrounds': {
        'safe_light': '#e6f4e6',        # Light green background
        'caution_light': '#fff8dc',     # Light yellow background  
        'danger_light': '#ffe6e6',      # Light red background
        'neutral_light': '#f5f5f5',     # Neutral light background
        'white': '#ffffff',             # Pure white
        'app_bg': '#f8f9fa',           # App background gray
    },
    
    # Text colors for accessibility
    'text': {
        'primary': '#000000',           # Primary black text
        'secondary': '#333333',         # Dark gray text
        'muted': '#6c757d',            # Muted gray text
        'white': '#ffffff',            # White text for dark backgrounds
        'light_gray': '#4a4a4a',       # Light gray text
    },
    
    # Extended palette for app-wide use
    'extended': {
        # Navigation and structural elements
        'nav_primary': '#5a7a8a',       # Primary navigation color (safe complement)
        'nav_secondary': '#6b5a8a',     # Secondary navigation (caution complement)
        'nav_accent': '#5a8a7a',        # Accent navigation (danger complement)
        
        # Status and feedback colors
        'success': '#28a745',           # Success messages (safe green)
        'warning': '#ffc107',           # Warning messages (caution yellow)
        'error': '#dc3545',             # Error messages (danger red)
        'info': '#5a7a8a',             # Info messages (blue-gray)
        
        # Interactive elements
        'button_primary': '#5a7a8a',    # Primary buttons
        'button_secondary': '#6b5a8a',  # Secondary buttons
        'button_success': '#28a745',    # Success buttons
        'button_danger': '#dc3545',     # Danger buttons
        
        # Borders and dividers
        'border_light': '#e0e0e0',      # Light borders
        'border_medium': '#ddd',        # Medium borders
        'border_dark': '#999',          # Dark borders
    }
}

# Semantic color mapping for different app sections
SECTION_COLORS = {
    'health': {
        'primary': APP_COLORS['core']['teal_gray'],              # Teal-gray
        'accent': APP_COLORS['extended']['error'],               # Error red accent
        'background': APP_COLORS['backgrounds']['danger_light'], # Light red bg
    },
    'feeding': {
        'primary': APP_COLORS['core']['blue_gray'],              # Blue-gray
        'accent': APP_COLORS['extended']['success'],             # Success green accent
        'background': APP_COLORS['backgrounds']['safe_light'],   # Light green bg
    },
    'growth': {
        'primary': APP_COLORS['core']['purple_gray'],            # Purple-gray
        'accent': APP_COLORS['extended']['warning'],             # Warning yellow accent
        'background': APP_COLORS['backgrounds']['caution_light'], # Light yellow bg
    },
    'settings': {
        'primary': APP_COLORS['text']['secondary'],              # Secondary text color
        'accent': APP_COLORS['text']['muted'],                   # Muted gray
        'background': APP_COLORS['backgrounds']['neutral_light'], # Light gray bg
    },
    'plants': {
        # Dynamic - uses safety-based colors from plant data
        'safe': {
            'primary': APP_COLORS['core']['blue_gray'],
            'accent': APP_COLORS['extended']['success'],
            'background': APP_COLORS['backgrounds']['safe_light'],
        },
        'caution': {
            'primary': APP_COLORS['core']['purple_gray'],
            'accent': APP_COLORS['extended']['warning'],
            'background': APP_COLORS['backgrounds']['caution_light'],
        },
        'toxic': {
            'primary': APP_COLORS['core']['teal_gray'],
            'accent': APP_COLORS['extended']['error'],
            'background': APP_COLORS['backgrounds']['danger_light'],
        }
    }
}

# CSS color variables for consistent styling
CSS_VARIABLES = """
:root {
    /* Primary Colors */
    --color-safe-green: #28a745;
    --color-caution-yellow: #ffc107;
    --color-danger-red: #dc3545;
    
    /* Header Colors */
    --color-header-green: #5a7a8a;
    --color-header-yellow: #6b5a8a;
    --color-header-red: #5a8a7a;
    --color-header-neutral: #9cafb7;
    
    /* Background Colors */
    --color-bg-safe: #e6f4e6;
    --color-bg-caution: #fff8dc;
    --color-bg-danger: #ffe6e6;
    --color-bg-neutral: #f5f5f5;
    --color-bg-app: #f8f9fa;
    
    /* Text Colors */
    --color-text-primary: #000000;
    --color-text-secondary: #333333;
    --color-text-muted: #6c757d;
    --color-text-white: #ffffff;
}
"""

def get_section_colors(section_name):
    """Get colors for a specific app section"""
    return SECTION_COLORS.get(section_name, SECTION_COLORS['settings'])

def get_plant_colors(safety_level):
    """Get colors for a specific plant safety level"""
    return SECTION_COLORS['plants'].get(safety_level, SECTION_COLORS['plants']['safe'])