#!/usr/bin/env python3
"""
Debug launcher for Tortoise Care Touch
Provides verbose logging and error tracking
"""

import sys
import os
import traceback
import logging
from datetime import datetime

# Set up debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def check_environment():
    """Check Python environment and dependencies"""
    print("=== TORTOISE CARE TOUCH DEBUG MODE ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Check required modules
    required_modules = [
        'kivy', 'kivymd', 'sqlite3', 'PIL', 'requests', 
        'dateutil', 'adafruit_io', 'emoji'
    ]
    
    print("\n=== DEPENDENCY CHECK ===")
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'PIL':
                import PIL
                print(f"✓ {module}: {PIL.__version__}")
            elif module == 'dateutil':
                import dateutil
                print(f"✓ {module}: {dateutil.__version__}")
            elif module == 'adafruit_io':
                import Adafruit_IO
                print(f"✓ {module}: Found")
            else:
                mod = __import__(module)
                version = getattr(mod, '__version__', 'Unknown')
                print(f"✓ {module}: {version}")
        except ImportError as e:
            print(f"✗ {module}: MISSING - {e}")
            missing_modules.append(module)
        except Exception as e:
            print(f"? {module}: ERROR - {e}")
    
    if missing_modules:
        print(f"\n⚠️  MISSING DEPENDENCIES: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies found!")
    return True

def check_files():
    """Check required files and directories"""
    print("\n=== FILE STRUCTURE CHECK ===")
    
    required_files = [
        'main.py',
        'database/db_manager.py',
        'screens/base_screen.py',
        'screens/home_screen.py',
        'screens/health_screen.py',
        'requirements.txt'
    ]
    
    required_dirs = [
        'database',
        'screens',
        'photos',
        'data'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}: MISSING")
            missing_files.append(file_path)
    
    missing_dirs = []
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/: MISSING")
            missing_dirs.append(dir_path)
    
    if missing_files or missing_dirs:
        print(f"\n⚠️  MISSING FILES: {missing_files}")
        print(f"⚠️  MISSING DIRS: {missing_dirs}")
        return False
    
    print("\n✓ All required files found!")
    return True

def check_database():
    """Check database connectivity"""
    print("\n=== DATABASE CHECK ===")
    
    try:
        from database.db_manager import DatabaseManager
        print("✓ DatabaseManager imported successfully")
        
        db = DatabaseManager()
        print("✓ DatabaseManager instance created")
        
        # Try to connect to database
        conn = db.get_connection()
        print("✓ Database connection established")
        
        # Check if tables exist
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if tables:
            print(f"✓ Found {len(tables)} database tables:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("⚠️  No tables found - database needs initialization")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        traceback.print_exc()
        return False

def start_app_with_debug():
    """Start the main application with debug logging"""
    print("\n=== STARTING APPLICATION ===")
    
    try:
        # Import Kivy with debug settings
        os.environ['KIVY_LOG_LEVEL'] = 'debug'
        
        # Import main application
        print("Importing main application...")
        from main import TortoiseCareApp
        print("✓ Main application imported")
        
        # Create and run app
        print("Creating application instance...")
        app = TortoiseCareApp()
        print("✓ Application instance created")
        
        print("Starting application...")
        app.run()
        
    except Exception as e:
        print(f"\n✗ APPLICATION ERROR: {e}")
        print("\n=== FULL TRACEBACK ===")
        traceback.print_exc()
        
        # Save error to file
        with open(f'crash_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w') as f:
            f.write(f"Tortoise Care Touch Crash Report\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"Python: {sys.version}\n")
            f.write(f"Working Directory: {os.getcwd()}\n\n")
            f.write("Traceback:\n")
            traceback.print_exc(file=f)
        
        return False

if __name__ == "__main__":
    success = True
    
    # Run all checks
    success &= check_environment()
    success &= check_files()
    success &= check_database()
    
    if success:
        print("\n✓ All checks passed! Starting application...")
        start_app_with_debug()
    else:
        print("\n✗ Some checks failed. Please fix the issues above before running.")
        sys.exit(1)