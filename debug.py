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
    """Check database connectivity and performance"""
    print("\n=== DATABASE CHECK ===")
    
    try:
        import time
        from database.db_manager import DatabaseManager
        print("✓ DatabaseManager imported successfully")
        
        start_time = time.time()
        db = DatabaseManager()
        init_time = time.time() - start_time
        print(f"✓ DatabaseManager instance created ({init_time:.3f}s)")
        
        # Try to connect to database
        start_time = time.time()
        conn = db.get_connection()
        connect_time = time.time() - start_time
        print(f"✓ Database connection established ({connect_time:.3f}s)")
        
        # Check if tables exist and record count
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if tables:
            print(f"✓ Found {len(tables)} database tables:")
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"  - {table[0]}: {count} records")
                except:
                    print(f"  - {table[0]}: unable to count")
        else:
            print("⚠️  No tables found - database needs initialization")
        
        # Test plant database loading time
        start_time = time.time()
        cursor.execute("SELECT * FROM plants")
        plants = cursor.fetchall()
        plant_time = time.time() - start_time
        print(f"✓ Plant database query: {len(plants)} plants ({plant_time:.3f}s)")
        
        if plant_time > 1.0:
            print("⚠️  Plant database loading is slow - consider indexing")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        traceback.print_exc()
        return False

def check_image_handling():
    """Check image directories and PIL performance"""
    print("\n=== IMAGE HANDLING CHECK ===")
    
    try:
        import time
        from PIL import Image
        print("✓ PIL imported successfully")
        
        # Check image directories
        image_dirs = [
            'photos',
            'photos/tortoises',
            'photos/plants',
            'photos/plants/leaves',
            'photos/plants/flowers',
            'photos/plants/full',
            'photos/growth'
        ]
        
        for img_dir in image_dirs:
            if os.path.exists(img_dir):
                files = os.listdir(img_dir)
                img_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
                print(f"✓ {img_dir}: {len(img_files)} images, {len(files)} total files")
                
                # Check for large images that could slow loading
                for img_file in img_files[:5]:  # Check first 5 images
                    try:
                        img_path = os.path.join(img_dir, img_file)
                        size = os.path.getsize(img_path)
                        if size > 1024 * 1024:  # > 1MB
                            print(f"  ⚠️  Large image: {img_file} ({size/1024/1024:.1f}MB)")
                    except:
                        pass
            else:
                print(f"✗ {img_dir}: MISSING")
        
        # Test PIL performance with a simple operation
        start_time = time.time()
        test_img = Image.new('RGB', (100, 100), color='red')
        pil_time = time.time() - start_time
        print(f"✓ PIL image creation test: {pil_time:.3f}s")
        
        if pil_time > 0.1:
            print("⚠️  PIL performance seems slow")
        
        return True
        
    except Exception as e:
        print(f"✗ Image handling error: {e}")
        traceback.print_exc()
        return False

def check_performance():
    """Check system performance and resource usage"""
    print("\n=== PERFORMANCE CHECK ===")
    
    try:
        import time
        
        # Basic performance check without psutil
        start_time = time.time()
        test_list = [i for i in range(10000)]
        cpu_test_time = time.time() - start_time
        print(f"✓ CPU performance test: {cpu_test_time:.3f}s")
        
        if cpu_test_time > 0.1:
            print("⚠️  CPU performance seems slow")
        
        # Check available disk space
        if hasattr(os, 'statvfs'):  # Unix/Linux
            statvfs = os.statvfs('.')
            free_bytes = statvfs.f_frsize * statvfs.f_bavail
            free_gb = free_bytes / (1024 * 1024 * 1024)
            print(f"✓ Available disk space: {free_gb:.1f}GB")
            
            if free_gb < 1:
                print("⚠️  Low disk space - less than 1GB available")
        
        # Try to get system info if available
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            print(f"✓ CPU usage: {cpu_percent}%")
            print(f"✓ Memory: {memory.percent}% used ({memory.available/1024/1024/1024:.1f}GB available)")
            
            if cpu_percent > 80:
                print("⚠️  High CPU usage detected")
            if memory.percent > 80:
                print("⚠️  High memory usage detected")
                
        except ImportError:
            print("? psutil not available - install with 'pip install psutil' for detailed system monitoring")
            
        return True
        
    except Exception as e:
        print(f"✗ Performance check error: {e}")
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
    success &= check_image_handling()
    success &= check_performance()
    
    if success:
        print("\n✓ All checks passed! Starting application...")
        start_app_with_debug()
    else:
        print("\n✗ Some checks failed. Please fix the issues above before running.")
        sys.exit(1)