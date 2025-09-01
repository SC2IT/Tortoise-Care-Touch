# Tortoise Care Touch - PySide6 Version

This is the PySide6/Qt version of the Tortoise Care Touch application, designed for better compatibility with Raspberry Pi OS and reliable icon/font rendering.

## Requirements

- Python 3.7+
- PySide6
- SQLite3 (included with Python)

## Installation

```bash
pip install PySide6
```

## Running the Application

### Desktop/Development
```bash
python main_qt.py
```

### Pi Touch Display (Fullscreen)
```bash
python main_qt.py --fullscreen
```

## Key Features

- **Reliable UI**: Native Qt widgets work perfectly on Pi OS
- **Touch-Friendly**: Large buttons and fonts optimized for touch displays
- **Emoji Icons**: Built-in emoji support that works reliably across platforms
- **Responsive**: Adapts to different screen sizes and orientations
- **Database**: SQLite backend for all tortoise care data

## Screens Implemented

- ✅ **Home Screen**: Main navigation with status display
- ✅ **Settings Main**: Category navigation for all settings
- ✅ **Health Screen**: Comprehensive health guides and emergency protocols
- 🚧 **Additional screens**: To be implemented

## Advantages over Kivy Version

1. **Better Pi OS compatibility**: Native Qt widgets render properly
2. **Reliable icons**: Emoji characters work consistently
3. **Professional appearance**: Native OS styling
4. **Touch optimization**: Built-in touch event handling
5. **Font support**: Better Unicode and emoji font rendering

## Architecture

- `main_qt.py`: Application entry point and window management
- `qt_screens/`: All screen implementations
- `qt_screens/base_screen.py`: Common UI components and styling
- `database/`: SQLite database management (shared with Kivy version)

This version maintains the same database and core functionality as the Kivy version while providing a much more reliable user interface for Pi Touch Display deployment.