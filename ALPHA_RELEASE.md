# 🐢 Tortoise Care Touch - Alpha Release v0.1.0

Welcome to the first alpha release of **Tortoise Care Touch** - a comprehensive touch-screen application for Hermann's tortoise care management!

## 🎯 **What's Working in Alpha**

### ✅ **Core Features Ready**
- **Touch-optimized interface** for Pi Touch Display 2 (720x1280)
- **Dynamic orientation detection** - automatically adapts to portrait/landscape
- **Feeding tracking system** - weight-based logging with plant database  
- **User management** - multi-user profiles with task assignments
- **Tortoise profiles** - individual care records and tracking
- **Settings management** - Adafruit.IO setup and configuration

### 🏗️ **Framework Complete**
- SQLite database with full schema for tortoise care data
- Pre-loaded with 10+ safe Hermann's tortoise plants
- Modular screen architecture for easy expansion
- Automated installation script for Raspberry Pi

## 🚀 **Quick Start**

### **Installation**
```bash
git clone https://github.com/SC2IT/Tortoise-Care-Touch.git
cd Tortoise-Care-Touch
python3 install.py
```

### **Launch**
```bash
python3 main.py
```

### **Test Orientation**
```bash
python3 test_orientation.py
```

## 🎮 **How to Use**

1. **First Run**: Application creates default user and empty database
2. **Add Users**: Settings → User Management → Add User
3. **Add Tortoises**: Settings → Tortoise Management → Add New Tortoise  
4. **Record Feeding**: Feed Tortoise → Select items, weights, notes
5. **Assign Tasks**: Settings → User Management → Assign Tasks
6. **Configure Habitat**: Settings → Adafruit.IO Settings (optional)

## 🔧 **Hardware Requirements**

- **Raspberry Pi 4** (2GB+ recommended)
- **Pi Touch Display 2** (720x1280 resolution)  
- **MicroSD card** (16GB+ recommended)
- **Optional**: Adafruit sensors for habitat monitoring

## ⚠️ **Alpha Limitations**

### **Not Yet Implemented**
- Health monitoring with online resources
- Real-time Adafruit.IO data collection
- Growth tracking with photo import
- Care reminder notifications
- Plant database with photos

### **Known Issues**
- Placeholder screens for health, habitat, growth, and reminders
- Task assignment saves but doesn't integrate with reminder system
- Feeding records save to database but recent feedings view not implemented

## 🛠️ **For Developers**

### **Architecture**
- `main.py` - Application entry point with orientation manager
- `database/` - SQLite database management and schema
- `screens/` - Modular UI screens inheriting from BaseScreen
- `utils/` - Orientation detection and management utilities

### **Key Classes**
- `OrientationManager` - Handles dynamic screen orientation
- `BaseScreen` - Orientation-aware base class for all screens
- `DatabaseManager` - SQLite operations and schema management

## 📋 **Roadmap to Beta**

### **Next Release (v0.2.0-beta)**
- [ ] Health monitoring integration
- [ ] Real-time Adafruit.IO habitat monitoring  
- [ ] Growth tracking with photo import
- [ ] Working care reminder system
- [ ] Plant database with photo references

## 🐛 **Found a Bug?**

Please report issues at: https://github.com/SC2IT/Tortoise-Care-Touch/issues

Include:
- Pi model and OS version
- Display orientation when issue occurred
- Steps to reproduce
- Screenshot if applicable

## 📞 **Support**

This alpha release is designed for:
- **Hermann's tortoise owners** wanting digital care tracking
- **Raspberry Pi enthusiasts** interested in touch applications
- **Python developers** looking at Kivy orientation management

---

**Happy tortoise caring!** 🐢✨

*This is an alpha release - expect bugs and missing features. Your feedback helps make it better!*