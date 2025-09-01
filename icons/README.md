# OpenMoji Icons for Tortoise Care Touch

This directory contains 41 essential PNG icons from [OpenMoji](https://openmoji.org) for the Tortoise Care Touch application.

## License
- **Graphics**: CC BY-SA 4.0 (Creative Commons Attribution-ShareAlike)
- **Created by**: HfG Schwäbisch Gmünd students and professors
- **Source**: https://openmoji.org

## Available Icons

### Basic UI & System
- `settings.png` - ⚙️ Application settings
- `back.png` - ← Navigation back button  
- `home.png` - 🏠 Home screen
- `info.png` - ℹ️ Information dialogs
- `x.png` - ❌ Close/cancel actions
- `search.png` - 🔍 Search functionality

### Users & People
- `user.png` - 👤 Single user profile
- `users.png` - 👥 Multiple users/user management

### Health & Care System
- `heart.png` - ❤️ General health/vital signs
- `medical.png` - 🩺 Medical checkups/veterinary
- `pill.png` - 💊 Medication tracking
- `emergency.png` - ⚠️ Emergency protocols/warnings
- `phone.png` - 📞 Contact veterinarian
- `clipboard.png` - 📋 Health records management
- `chart.png` - 📊 Health data visualization
- `notes.png` - 📝 Care notes and observations

### Growth Tracking & Photos
- `camera.png` - 📷 Photo capture/import
- `ruler.png` - 📏 Size measurements
- `scale.png` - ⚖️ Weight tracking
- `trending-up.png` - 📈 Growth charts/progress

### Environmental Monitoring (Adafruit.IO)
- `thermometer.png` - 🌡️ Temperature monitoring
- `droplet.png` - 💧 Humidity monitoring
- `activity.png` - 📶 Sensor connectivity/data
- `bar-chart.png` - 📊 Environmental data graphs

### Care Reminders & Scheduling
- `calendar.png` - 📅 Scheduling system
- `clock.png` - ⏰ Timing and reminders
- `bell.png` - 🔔 Notifications
- `check.png` - ✅ Completed tasks

### Food & Plant Database
- `tortoise.png` - 🐢 Tortoise management
- `apple.png` - 🍎 Food items
- `leaf.png` - 🍃 Plant identification
- `plant.png` - 🌱 Seedlings/young plants
- `salad.png` - 🥗 Vegetables/greens

### Navigation & Actions
- `plus.png` - ➕ Add new entries
- `edit.png` - ✏️ Edit records
- `trash.png` - 🗑️ Delete items
- `save.png` - 💾 Save data
- `upload.png` - 📤 Export data
- `download.png` - 📥 Import data

### Data & Technology
- `database.png` - 💾 Database operations
- `wifi.png` - 📶 Network connectivity

## Usage in Code

### Using the Icon Widget Manager
```python
from utils.icon_widgets import icon_widget

# Create a simple icon
icon = icon_widget.create_icon('tortoise', size=(32, 32))

# Create button content with icon and text
button_content = icon_widget.create_icon_button_content(
    'medical', 'Health Check', icon_size=(24, 24)
)
```

### Direct Icon Manager Usage
```python
from utils.openmoji_icons import OpenMojiIconManager

manager = OpenMojiIconManager()
icon_path = manager.get_icon_path('heart')  # Returns full path to heart.png
```

## Icon Specifications
- **Format**: PNG with transparency
- **Color**: Full color OpenMoji style
- **Size**: Various sizes available (typically 72x72px from OpenMoji)
- **Optimization**: Suitable for Raspberry Pi Touch Display performance
- **Quality**: High resolution for crisp display on Pi Touch Display 2

## Attribution
Icons provided by OpenMoji – the open-source emoji and icon project.
License: CC BY-SA 4.0. https://openmoji.org