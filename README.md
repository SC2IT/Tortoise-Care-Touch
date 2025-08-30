# 🐢 Tortoise Care Touch

A comprehensive touch-screen tortoise care tracking application designed for **Raspberry Pi 4** with **Pi Touch Display 2**. Built specifically for Hermann's tortoise care with multi-user support, habitat monitoring, and dynamic orientation support.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Kivy](https://img.shields.io/badge/UI-Kivy-brightgreen.svg)](https://kivy.org/)

> **🚀 Major Release v0.2.0-alpha**: Comprehensive health monitoring system with emergency protocols and 60+ plant database! See [CHANGELOG.md](CHANGELOG.md) for full release notes.

## ✨ Alpha Features (Working Now)

### 🏥 **Health Monitoring & Care Guides** ✅ NEW!
- **Emergency protocols** with step-by-step poisoning response procedures
- **Signs of healthy tortoise** interactive guide with physical and behavioral indicators
- **Warning signs and illness detection** guide for early intervention
- **Hermann's tortoise care guide** with species-specific requirements
- **Seasonal care recommendations** including hibernation guidance
- All content sourced from The Tortoise Table and veterinary authorities

### 🚨 **Emergency Response System** ✅ NEW!
- **Red alert emergency button** for immediate access to poisoning protocols
- **Acute and cumulative poisoning symptoms** identification
- **Emergency veterinary contact integration** (Settings → Connections)
- **Step-by-step response procedures** from authoritative sources

### 🌿 **Comprehensive Plant Database** ✅ EXPANDED!
- **60+ plants** with detailed safety classifications (up from 10)
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

### 🐢 **Tortoise Profiles** ✅
- Individual tortoise management (name, sex, weight)
- Species tracking (default Hermann's tortoise)
- Growth monitoring framework

### 📱 **Touch Interface** ✅
- Optimized for Pi Touch Display 2 (720x1280)
- **Dynamic orientation detection** - auto-adapts portrait ↔ landscape
- **Enhanced emoji support** for proper icon rendering on Pi display
- Large, finger-friendly buttons and minimal typing
- Touch-responsive navigation and forms

### ⚙️ **Settings & Setup** ✅
- **Individual settings screens** for each category (no more crashes!)
- User Management, Tortoise Management, Connections, Database sections
- Adafruit.IO integration configuration
- Automated Pi installation with desktop shortcuts

### ℹ️ **About & Attribution** ✅ NEW!
- **Comprehensive source citations** for all plant and health data
- **Technical framework acknowledgments** and dependencies
- **Privacy policy** and data handling transparency
- **License information** and contribution guidelines

## 🚧 Beta Features (Coming Soon)

### 📊 **Health Records Management** 🔄
- Digital vet visit records and health observation tracking
- Photo documentation and medication scheduling

### 🌡️ **Habitat Monitoring** 🔄
- Real-time temperature and humidity via Adafruit.IO
- Alert system for out-of-range conditions
- Historical data logging and charts

### 📈 **Growth Tracking** 🔄
- Photo import from iPhone/mobile devices
- Weight and size measurement tracking
- Growth charts and progress visualization

### ⏰ **Care Reminders** 🔄
- Working task scheduling and notifications
- Daily, weekly, monthly care routines
- Task completion tracking

### 🌿 **Enhanced Plant Database** 🔄
- Plant photos (leaves, flowers, full plant)
- Visual plant identification guide
- Interactive feeding recommendations

## Hardware Requirements

- Raspberry Pi 4 (2GB+ recommended) 
- Raspberry Pi Touch Display 2 (7" 720x1280 portrait)
- MicroSD card (16GB+ recommended)
- Optional: Adafruit sensors for habitat monitoring

## Installation

1. **Clone or download** this repository to your Raspberry Pi as `Tortoise-Care-Touch`
2. **Navigate to the project directory**
   ```bash
   cd Tortoise-Care-Touch
   ```
3. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Initialize the application**:
   ```bash
   # Create directories
   mkdir -p photos/{tortoises,plants/{leaves,flowers,full},growth}
   mkdir -p data/backups
   
   # Initialize database
   python -c "from database.db_manager import DatabaseManager; db = DatabaseManager(); db.initialize_database()"
   
   # Start the application
   python main.py
   ```

## Automated Installation Script

For convenience, you can also use the installation script (will handle virtual environment setup):
```bash
python3 install.py
```

The installer will:
- Create virtual environment automatically
- Check Python version compatibility
- Install required dependencies (including emoji support)
- Set up directory structure
- Initialize the SQLite database
- Create desktop shortcuts
- Offer autostart configuration

## Running the Application

After installation, always activate the virtual environment first:

```bash
cd Tortoise-Care-Touch
source venv/bin/activate
python main.py
```

### Debug Mode
If the application fails to start, use debug mode for detailed diagnostics:

```bash
source venv/bin/activate
python debug.py
```

Debug mode provides:
- Comprehensive dependency checking
- File structure validation
- Database connectivity testing
- Verbose startup logging
- Crash report generation

To deactivate the virtual environment when done:
```bash
deactivate
```

## Configuration

### Adafruit.IO Setup
1. Create an account at [io.adafruit.com](https://io.adafruit.com)
2. Get your API key and username
3. Create feeds for temperature and humidity
4. Configure settings in the application Settings screen

### Photo Import
- Set up a folder for automatic photo import (default: `/home/pi/tortoise_photos`)
- Photos copied to this folder will be automatically imported
- Supports iPhone photo sharing via various methods

### Pi Touch Display 2 Optimization
The application is optimized for Pi Touch Display 2 with:
- Large, finger-friendly buttons (720x1280 portrait resolution)
- Portrait layout with single-column navigation for easier touch
- Minimal text input requirements
- Scrollable lists and forms optimized for vertical space
- Popup confirmations for important actions
- Improved touch response and gesture recognition
- Multi-touch disabled for better single-touch accuracy

## Usage

### First Time Setup
1. **Add Users**: Set up family members who will care for the tortoises
2. **Add Tortoises**: Register your Hermann's tortoises with basic info
3. **Configure Habitat Monitoring**: Set up Adafruit.IO integration
4. **Review Plant Database**: Familiarize yourself with safe plants

### Daily Use
1. **Record Feedings**: Track what and how much you feed
2. **Monitor Habitat**: Check temperature/humidity readings
3. **Complete Reminders**: Mark off daily care tasks
4. **Add Observations**: Note any health or behavior changes

### Weekly/Monthly Tasks
1. **Weight Measurements**: Record growth data
2. **Photo Documentation**: Take progress photos
3. **Health Check**: Schedule and record vet visits
4. **Review Data**: Analyze feeding patterns and growth

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

### Adding New Features
The application uses a modular screen-based architecture:
- `screens/` - Individual screen implementations
- `database/` - Database management and queries
- `main.py` - Application entry point and navigation

### Customization
- Modify plant database for other tortoise species
- Adjust UI colors and sizes in screen files
- Add custom sensor integrations
- Extend reminder system for specialized care

## Troubleshooting

### Common Issues
- **Application won't start**: Run `python debug.py` for detailed diagnostics
- **Missing dependencies**: Use virtual environment and check `pip install -r requirements.txt`
- **Touch not working**: Check screen calibration and Kivy touch settings
- **Database errors**: Ensure proper permissions and disk space
- **Sensor connectivity**: Verify Adafruit.IO credentials and network
- **Photo import**: Check folder permissions and file formats

### Support
This application was designed specifically for Hermann's tortoise care. For issues or feature requests, please check the documentation or modify the code as needed for your setup.

## License

This project is designed for personal use in tortoise care. Feel free to modify and adapt for your specific needs.

---

*Built with ❤️ for Hermann's tortoise care*