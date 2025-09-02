# 🐢 Tortoise Care Touch

A comprehensive touch-screen tortoise care tracking application designed for **Raspberry Pi 4** with **Pi Touch Display 2**. Built specifically for Hermann's tortoise care with multi-user support, habitat monitoring, and reliable Qt interface.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/UI-PySide6-brightgreen.svg)](https://doc.qt.io/qtforpython/)

> **🚀 Version 0.3.0-alpha**: PySide6/Qt conversion for reliable Pi OS compatibility! Still in alpha development with core features working.

## ✨ Alpha Features (Working Now)

### 🖥️ **Reliable Qt Interface** ✅ NEW!
- **PySide6/Qt native widgets** - No more broken layouts or missing text
- **Touch-optimized interface** with large 60-80px buttons for Pi Touch Display
- **Professional styling** with consistent color schemes and native OS appearance
- **Emoji icon support** that works reliably across all Pi OS versions
- **Responsive design** adapts to different orientations and screen sizes

### 🏥 **Health Monitoring & Care Guides** ✅
- **Emergency protocols** with step-by-step poisoning response procedures
- **Signs of healthy tortoise** interactive guide with physical and behavioral indicators
- **Warning signs and illness detection** guide for early intervention
- **Hermann's tortoise care guide** with species-specific requirements
- **Comprehensive scrollable dialogs** with detailed veterinary information
- All content sourced from The Tortoise Table and veterinary authorities

### 🚨 **Emergency Response System** ✅
- **Red alert emergency button** for immediate access to poisoning protocols
- **Acute and cumulative poisoning symptoms** identification
- **Emergency veterinary contact integration** (Settings → Connections)
- **Step-by-step response procedures** from authoritative sources

### 🌿 **Comprehensive Plant Database** ✅
- **60+ plants** with detailed safety classifications
- **Daily safe foods, caution plants, and toxic warnings**
- **Scientific names, nutrition info, and feeding frequencies**
- **Color-coded safety indicators** throughout the feeding system
- **Proper source attribution** to The Tortoise Table plant database

### 🍃 **Feeding Tracking** ✅
- Weight-based feeding session logging
- **Enhanced plant safety indicators** with green/yellow/red coding
- Supplement tracking (calcium, vitamins, etc.)
- Multi-user feeding logs with behavior notes
- "Ate well" and "new food introduced" tracking

### 👥 **User Management** ✅
- Multi-user profiles for family members
- Task assignment system for care responsibilities
- Individual user feeding and care records

### 🐢 **Tortoise Profiles** ✅ ENHANCED!
- **Complete tortoise management** with physical descriptions for identification
- **Photo upload system** accessible from mobile phones via local network
- **Large 400x400px photos** with rounded corners for accurate tortoise identification
- **Birthday/acquisition date handling** with checkbox for unknown birthdates
- Species tracking (default Hermann's tortoise) with subspecies support
- **Edit and deactivate** functionality for comprehensive profile management

### 📱 **Touch Interface** ✅ ENHANCED!
- **Optimized for 7-inch landscape touch displays** (1280x720 resolution)
- **Native Qt touch handling** with proper gesture recognition
- **Large, finger-friendly buttons** (60px+ height) and minimal typing required
- **Professional Qt styling** with hover effects and touch feedback
- **Tortoise selection screens** with large photos for accurate identification
- **Mobile photo upload interface** for seamless device integration

### ⚙️ **Settings & Configuration** ✅
- **Individual settings screens** for each category
- User Management, Tortoise Management, Connections, Database sections
- Adafruit.IO integration configuration
- Version information and system status display

## 🚧 Upcoming Features

### 📊 **Health Records Management** ✅ NEW!
- **Complete health records system** with CRUD operations
- **Digital vet visit records** and health observation tracking
- **Photo documentation** and medication scheduling
- **Priority-based tracking** (urgent, high, medium, low)
- **Multi-user health record management** with user attribution
- **Comprehensive health summaries** and statistics tracking

### 🌡️ **Habitat Monitoring** ✅ NEW!
- **Habitat monitoring interface** with placeholder for sensor integration
- Real-time temperature and humidity via Adafruit.IO (configuration ready)
- Alert system for out-of-range conditions
- Historical data logging and charts framework

### 📈 **Growth Tracking** ✅ NEW!
- **Growth tracking interface** with measurement recording system
- Photo import from mobile devices via upload server
- Weight and size measurement tracking framework
- Growth charts and progress visualization (ready for data)

### ⏰ **Care Reminders** ✅ NEW!
- **Care reminders management system** with task scheduling
- Daily, weekly, monthly care routines framework
- Task completion tracking and notification system
- Multi-user reminder assignments

## Hardware Requirements

- Raspberry Pi 4 (2GB+ recommended) 
- 7-inch Touch Display (1280x720 landscape orientation)
- MicroSD card (16GB+ recommended) 
- WiFi connection for mobile photo uploads
- Optional: Adafruit sensors for habitat monitoring

## Installation

### Quick Start (Recommended)

1. **Set up virtual environment** on your Pi:
   ```bash
   mkdir ~/tortoise-care
   cd ~/tortoise-care
   python3 -m venv tortoise-env
   source tortoise-env/bin/activate
   ```

2. **Install PySide6**:
   ```bash
   pip install PySide6
   ```

3. **Clone and run**:
   ```bash
   git clone https://github.com/SC2IT/Tortoise-Care-Touch.git
   cd Tortoise-Care-Touch
   python main_qt.py --fullscreen
   ```

### Detailed Installation

See [INSTALL_PI.md](INSTALL_PI.md) for comprehensive Pi installation instructions including:
- System dependency setup
- Virtual environment configuration
- Troubleshooting guide
- Auto-start service setup

## Running the Application

### Standard Mode
```bash
cd ~/tortoise-care/Tortoise-Care-Touch
source ~/tortoise-care/tortoise-env/bin/activate
python main_qt.py
```

### Pi Touch Display (Fullscreen)
```bash
python main_qt.py --fullscreen
```

### Development Dependencies
If you need to install additional packages:
```bash
pip install -r requirements.txt
```

## Configuration

### Database Setup
The application automatically creates an SQLite database on first run. No manual database setup required.

### Adafruit.IO Setup
1. Create an account at [io.adafruit.com](https://io.adafruit.com)
2. Get your API key and username
3. Create feeds for temperature and humidity
4. Configure settings in the application Settings screen

### Mobile Photo Upload System ✅ NEW!
The application includes a built-in web server for easy photo uploads from mobile devices:

1. **Automatic server startup** - Photo server starts automatically with the application
2. **Mobile access** - Connect to the Pi from your phone via WiFi
3. **Simple upload interface** - Drag and drop or browse to upload photos
4. **Direct tortoise association** - Photos are automatically linked to selected tortoises
5. **Local network only** - Secure, no internet required

**How to use:**
- Note the server URL displayed when the app starts (e.g., http://192.168.1.100:5555)
- Visit this URL on your phone's web browser
- Select tortoise and upload photos directly

## Database Structure

The application uses SQLite with tables for:
- Users and tortoise profiles
- Feeding records and plant database  
- Health records and medications
- Growth measurements and photos
- Habitat sensor readings
- Care reminders and tasks
- Application settings

## Development

### Architecture
- `main_qt.py` - Main PySide6 application entry point
- `qt_screens/` - All screen implementations using Qt widgets
- `qt_screens/base_screen.py` - Common UI components and styling
- `database/` - SQLite database management and queries
- `utils/` - Utility functions and helpers

### Adding New Features
The application uses a modular screen-based architecture with Qt's signal/slot system for navigation and data updates.

## Advantages Over Previous Versions

✅ **Reliable Rendering**: Native Qt widgets eliminate UI crashes and broken layouts  
✅ **Professional Appearance**: Native OS styling with consistent theming  
✅ **Better Touch Support**: Proper Qt touch event handling  
✅ **Emoji Icons**: Built-in Unicode support works across all Pi OS versions  
✅ **Performance**: More efficient memory usage and faster rendering  
✅ **Maintainability**: Clean Qt architecture with proper separation of concerns  

## Troubleshooting

### Common Issues
- **PySide6 installation fails**: Use virtual environment and see [INSTALL_PI.md](INSTALL_PI.md)
- **Application won't start**: Check Python version and dependencies
- **Touch not working**: Verify Pi Touch Display drivers and calibration
- **Database errors**: Ensure proper file permissions and disk space
- **Sensor connectivity**: Verify Adafruit.IO credentials and network

### Alternative UI Frameworks
If PySide6 doesn't work on your system:
- **PyQt5**: `sudo apt install python3-pyqt5`
- **Tkinter**: Usually pre-installed with Python

### Support
This application is designed specifically for Hermann's tortoise care. For issues or feature requests, please check the documentation or modify the code as needed for your setup.

## License

This project is designed for personal use in tortoise care. Feel free to modify and adapt for your specific needs.

---

*Built with ❤️ for Hermann's tortoise care using PySide6/Qt*