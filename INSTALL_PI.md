# Raspberry Pi Installation Guide

## Step 1: Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install python3-full python3-venv python3-pip -y

# Optional: Install Qt5 development tools (may help with PySide6)
sudo apt install qt5-default qttools5-dev-tools -y
```

## Step 2: Create Virtual Environment

```bash
# Create project directory
mkdir ~/tortoise-care
cd ~/tortoise-care

# Create virtual environment
python3 -m venv tortoise-env

# Activate virtual environment
source tortoise-env/bin/activate
```

## Step 3: Install Python Dependencies

```bash
# With virtual environment activated
pip install PySide6

# If PySide6 fails, try these alternatives:
pip install PyQt5    # Fallback option 1
# OR
pip install tkinter  # Fallback option 2 (usually pre-installed)
```

## Step 4: Clone and Run Application

```bash
# Clone the repository
git clone https://github.com/SC2IT/Tortoise-Care-Touch.git
cd Tortoise-Care-Touch

# Run the application
python main_qt.py --fullscreen
```

## Step 5: Auto-Start on Boot (Optional)

Create a systemd service:

```bash
sudo nano /etc/systemd/system/tortoise-care.service
```

Add this content:
```ini
[Unit]
Description=Tortoise Care Touch App
After=graphical.target

[Service]
Type=simple
User=pi
Environment=DISPLAY=:0
WorkingDirectory=/home/pi/tortoise-care/Tortoise-Care-Touch
ExecStart=/home/pi/tortoise-care/tortoise-env/bin/python main_qt.py --fullscreen
Restart=always

[Install]
WantedBy=graphical.target
```

Enable the service:
```bash
sudo systemctl enable tortoise-care.service
sudo systemctl start tortoise-care.service
```

## Troubleshooting

If PySide6 installation fails:

### Option A: Use system Qt packages
```bash
sudo apt install python3-pyqt5
# Then modify main_qt.py to use PyQt5 instead
```

### Option B: Use Tkinter (most reliable)
```bash
# Tkinter is usually pre-installed
python3 -c "import tkinter; print('Tkinter available')"
```

### Option C: Use system packages (not recommended)
```bash
# Only if virtual environment doesn't work
pip install PySide6 --break-system-packages
```

## Virtual Environment Commands

```bash
# Activate environment
source ~/tortoise-care/tortoise-env/bin/activate

# Deactivate environment
deactivate

# Run app from anywhere
~/tortoise-care/tortoise-env/bin/python ~/tortoise-care/Tortoise-Care-Touch/main_qt.py --fullscreen
```