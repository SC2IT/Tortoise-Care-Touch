# 🐢 Tortoise Care Touch

A comprehensive touch-screen tortoise care tracking application designed for **Raspberry Pi 4** with **Pi Touch Display 2**. Built specifically for Hermann's tortoise care with multi-user support, habitat monitoring, and dynamic orientation support.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Kivy](https://img.shields.io/badge/UI-Kivy-brightgreen.svg)](https://kivy.org/)

> **🚀 Alpha Release v0.1.0**: Core features working! See [ALPHA_RELEASE.md](ALPHA_RELEASE.md) for current status and limitations.

## ✨ Alpha Features (Working Now)

### 🍃 **Feeding Tracking** ✅
- Weight-based feeding session logging
- Pre-loaded database of 10+ safe Hermann's tortoise plants
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
- Large, finger-friendly buttons and minimal typing
- Touch-responsive navigation and forms

### ⚙️ **Settings & Setup** ✅
- Adafruit.IO integration configuration
- User and tortoise management interfaces
- Automated Pi installation with desktop shortcuts

## 🚧 Beta Features (Coming Soon)

### 🏥 **Health Monitoring** 🔄
- Vet visit records and health observations
- Online resources integration for Hermann's tortoise care
- Photo documentation and priority alerts

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
- Expanded nutritional information
- Visual plant identification guide

## Hardware Requirements

- Raspberry Pi 4 (2GB+ recommended) 
- Raspberry Pi Touch Display 2 (7" 720x1280 portrait)
- MicroSD card (16GB+ recommended)
- Optional: Adafruit sensors for habitat monitoring

## Installation

1. **Clone or download** this repository to your Raspberry Pi as `tortoise-care-touch`
2. **Navigate to the project directory**
   ```bash
   cd tortoise-care-touch
   ```
3. **Run the installation script**:
   ```bash
   python3 install.py
   ```

The installer will:
- Check Python version compatibility
- Install required dependencies
- Set up directory structure
- Initialize the SQLite database
- Create desktop shortcuts
- Offer autostart configuration

## Manual Installation

If you prefer manual setup:

```bash
# Install dependencies
pip3 install -r requirements.txt

# Create directories
mkdir -p photos/{tortoises,plants/{leaves,flowers,full},growth}
mkdir -p data/backups

# Initialize database
python3 -c "from database.db_manager import DatabaseManager; db = DatabaseManager(); db.initialize_database()"

# Start the application
python3 main.py
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