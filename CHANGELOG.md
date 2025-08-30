# Changelog

All notable changes to Tortoise Care Touch will be documented in this file.

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