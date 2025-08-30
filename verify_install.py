#!/usr/bin/env python3
"""
Quick verification script for Tortoise Care Touch installation
Run this to check if everything is set up correctly
"""

import os
import sys
import sqlite3

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required. Current:", sys.version)
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required = ['kivy', 'sqlite3']
    missing = []
    
    for package in required:
        try:
            if package == 'sqlite3':
                import sqlite3
                print("✅ SQLite3 available")
            elif package == 'kivy':
                import kivy
                print(f"✅ Kivy {kivy.__version__}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} not found")
    
    return len(missing) == 0

def check_directories():
    """Check if required directories exist"""
    dirs = ['database', 'screens', 'utils']
    all_good = True
    
    for directory in dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/ directory")
        else:
            print(f"❌ {directory}/ directory missing")
            all_good = False
    
    return all_good

def check_main_files():
    """Check if main application files exist"""
    files = ['main.py', 'requirements.txt', 'install.py', 'database/db_manager.py']
    all_good = True
    
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_good = False
    
    return all_good

def test_database():
    """Test database functionality"""
    try:
        from database.db_manager import DatabaseManager
        db = DatabaseManager("test_verify.db")
        db.initialize_database()
        
        # Test basic operations
        users = db.get_users()
        plants = db.get_plants()
        
        print(f"✅ Database working ({len(users)} users, {len(plants)} plants)")
        
        # Clean up
        db.close()
        if os.path.exists("test_verify.db"):
            os.remove("test_verify.db")
            
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_orientation_manager():
    """Test orientation detection system"""
    try:
        from utils.orientation_manager import OrientationManager
        om = OrientationManager()
        orientation = om.current_orientation
        config = om.get_layout_config()
        
        print(f"✅ Orientation Manager working (current: {orientation})")
        return True
    except Exception as e:
        print(f"❌ Orientation Manager error: {e}")
        return False

def main():
    print("🐢 Tortoise Care Touch - Installation Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
        ("Main Files", check_main_files),
        ("Database", test_database),
        ("Orientation Manager", test_orientation_manager)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        if check_func():
            passed += 1
        
    print(f"\n{'='*50}")
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Installation verified! Ready to run:")
        print("   python3 main.py")
    else:
        print("⚠️  Some issues found. Try running:")
        print("   python3 install.py")

if __name__ == "__main__":
    main()