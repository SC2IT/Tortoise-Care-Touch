# Changelog

All notable changes to Tortoise Care Touch will be documented in this file.

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