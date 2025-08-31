# Changelog

All notable changes to Tortoise Care Touch will be documented in this file.

## [0.2.2-alpha] - 2024-08-30

### Critical Bug Fix

### Fixed
- **Health Screen Crash**: Fixed TypeError in button callbacks that was causing app crashes
  - All health screen method callbacks now properly handle the `instance` parameter
  - Emergency protocols, health guides, and care guides now work without crashing
  - Resolved "takes 1 positional argument but 2 were given" error

### Technical
- Added `instance=None` parameter to all health screen callback methods
- Improved button callback handling throughout the health monitoring system

## [0.2.1-alpha] - 2024-08-30

### Performance & Debugging Update

### Added
- **Enhanced Debug Tools**: Comprehensive performance analysis in debug.py
  - Database query timing and optimization detection
  - Image handling performance testing and large file detection
  - System resource monitoring (CPU, memory, disk usage)
  - PIL performance testing for image processing bottlenecks

- **Performance-Optimized Lite Version** (main_lite.py)
  - Progressive loading with immediate startup screen
  - Essential screens (Home, Feeding) load first for instant usability
  - Background loading of remaining screens while app is in use
  - Graphics optimizations: 30fps limit, disabled vsync, SDL2 backend
  - Reduced memory footprint and faster initialization

### Improved
- **Debug Script Performance Analysis**: Now measures exact timing for all operations
  - Database connection and query benchmarking
  - Plant database loading time analysis (60+ plants)
  - Image directory scanning with size warnings for large files
  - System performance baseline testing

### Technical
- **Optimized App Architecture**: Lite version uses progressive loading pattern
- **Background Screen Loading**: Non-essential screens load asynchronously
- **Performance Monitoring**: Enhanced debug output with millisecond timing
- **Resource Usage Analysis**: CPU, memory, and storage monitoring integration
- **Graphics Backend Optimization**: SDL2 and OpenGL configuration for better performance

### Fixed
- **Slow Loading Issues**: Lite version provides immediate responsiveness
- **Image Handling Performance**: Debug tools identify problematic large image files
- **Database Performance**: Timing analysis helps identify slow queries
- **System Resource Bottlenecks**: Enhanced monitoring for performance issues

## [0.2.0-alpha] - 2024-08-30

### Major Feature Release - Health Monitoring & Care Guides

### Added
- **Comprehensive Health Monitoring System**
  - Emergency protocols for poisoning and critical situations
  - Signs of healthy tortoise interactive guide with physical and behavioral indicators
  - Warning signs and illness detection guide
  - Hermann's tortoise species-specific care guide
  - Seasonal care recommendations and hibernation guidance

- **Emergency Response Features**
  - Red alert emergency protocols button for immediate access
  - Step-by-step poisoning response procedures from The Tortoise Table
  - Emergency veterinary contact integration (Settings → Connections)
  - Acute and cumulative poisoning symptom identification

- **Comprehensive Plant Database (60+ Plants)**
  - Expanded from 10 to 60+ plants with detailed safety classifications
  - Daily safe foods, caution plants, and toxic plant warnings
  - Scientific names, nutrition information, and feeding frequencies
  - Color-coded safety indicators (green/yellow/red) throughout feeding system

- **About Page with Full Attribution**
  - Comprehensive source citations for all plant and health data
  - Proper attribution to The Tortoise Table, Tortoise Trust, and veterinary sources
  - Technical framework acknowledgments and licensing information
  - Privacy policy and data handling transparency

- **Enhanced UI with Emoji Support**
  - Added emoji dependency for proper icon rendering on Pi display
  - Consistent iconography throughout health and feeding systems
  - Visual indicators for plant safety levels and emergency protocols

### Improved
- **Individual Settings Screens**: Complete separation of settings categories to prevent navigation crashes
- **Enhanced Plant Integration**: Plant safety indicators now appear in feeding system with proper color coding
- **Source-Based Information**: All health and plant data properly cited with authoritative sources

### Technical
- Added emoji>=2.2.0 dependency for cross-platform icon support
- Modular health screen architecture with popup-based detailed guides
- Comprehensive database schema updates for expanded plant information
- BaseScreen inheritance for consistent UI behavior across new screens
- **Debug Tools**: Added debug.py with comprehensive system diagnostics
- **Enhanced Logging**: Verbose logging in main.py for troubleshooting
- **Virtual Environment Support**: Updated installation for modern Python standards

### Sources & Attribution
- Plant Database: The Tortoise Table (thetortoisetable.org.uk)
- Health Monitoring: The Tortoise Table health guides and poisoning protocols
- Veterinary Standards: Association of Reptilian and Amphibian Veterinarians (ARAV)
- Species Care: Tortoise Trust and World Chelonian Trust guidelines

## [0.1.2-alpha] - 2024-08-30

### Improved
- **UI/UX for 7" Display**: Significantly increased font sizes across the entire application
  - Portrait: Large 28sp, Medium 22sp, Small 18sp (up from 20sp/16sp/14sp)
  - Landscape: Large 24sp, Medium 20sp, Small 16sp (up from 18sp/14sp/12sp)
- **Settings Menu Redesign**: Complete overhaul to eliminate scrolling
  - New main settings screen with 4 large category buttons
  - Separate sections: User Management, Tortoise Management, Connections, Database
  - Clear navigation with descriptive subtitles and icons
- **Touch Targets**: Increased button heights for better finger accessibility
  - Portrait buttons: 70px height (up from 60px)
  - Landscape buttons: 60px height (up from 50px)
- **Better Visual Hierarchy**: Improved spacing and layout proportions for 7" screens

### Added
- **Settings Categories**: Organized settings into logical sections to avoid overwhelming single screen
- **Version Display**: Settings now show current version and system status
- **Breadcrumb Navigation**: Clear back button paths between settings sections

### Technical
- Enhanced BaseScreen orientation management with new font size calculations
- Improved OrientationManager with better layout configurations for readability
- Settings architecture now supports modular category screens

## [0.1.1-alpha] - 2024-08-30

### Fixed
- **Orientation Detection**: Fixed window resize callback signature compatibility with newer Kivy versions
- Resolved crash on Pi Touch Display 2 during window resize events
- Improved error handling for orientation detection system

### Technical
- Updated `OrientationManager._on_window_resize()` to handle Kivy's size parameter correctly
- Better compatibility with Raspberry Pi OS and system-installed Kivy packages

## [0.1.0-alpha] - 2024-08-30

### Added
- **Core Application Framework**
  - Python Kivy-based touch interface optimized for Pi Touch Display 2
  - SQLite database with comprehensive schema for tortoise care data
  - Modular screen-based architecture for easy expansion

- **Dynamic Orientation Support**
  - Automatic detection of portrait (720x1280) and landscape (1280x720) orientations
  - Real-time UI adaptation with orientation changes
  - Touch-optimized layouts for both orientations

- **Feeding Tracking System**
  - Weight-based feeding records with plant and supplement tracking
  - Pre-loaded database of Hermann's tortoise safe plants
  - Multi-user feeding logs with behavior notes
  - Session tracking with "ate well" and "new food introduced" indicators

- **User Management**
  - Multi-user system with individual profiles
  - Task assignment system for care responsibilities
  - User-specific feeding and care records

- **Tortoise Management**
  - Individual tortoise profiles with species, sex, weight tracking
  - Growth monitoring capabilities
  - Health record framework

- **Settings & Configuration**
  - Adafruit.IO integration setup for habitat monitoring
  - User and tortoise management interfaces
  - Persistent settings storage

### Technical Features
- Touch-friendly UI with large buttons and minimal text input
- Responsive design adapting to screen orientation
- SQLite database with proper relationships and constraints
- Modular architecture for future feature expansion

### Installation
- Automated installation script for Raspberry Pi
- Desktop shortcuts and autostart configuration
- Dependency management and environment setup

## Coming Soon (Beta Features)
- Health monitoring with online resources integration  
- Real-time Adafruit.IO habitat monitoring
- Growth tracking with photo import from iPhone
- Care reminder and task scheduling system
- Hermann's tortoise plant database with photos