import sqlite3
import os
from datetime import datetime, date
from typing import Optional, List, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = "tortoise_care.db"):
        self.db_path = db_path
        self.connection = None
        
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                email TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tortoises table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tortoises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT DEFAULT "Hermann's Tortoise",
                subspecies TEXT,
                sex TEXT,
                birth_date DATE,
                acquisition_date DATE,
                current_weight REAL,
                notes TEXT,
                photo_path TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Plants database
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                scientific_name TEXT,
                safety_level TEXT CHECK(safety_level IN ('safe', 'caution', 'toxic')),
                nutrition_notes TEXT,
                feeding_frequency TEXT,
                leaf_photo_path TEXT,
                flower_photo_path TEXT,
                plant_photo_path TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Feeding records
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feeding_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tortoise_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                feeding_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_weight REAL,
                notes TEXT,
                ate_well BOOLEAN,
                new_food_introduced BOOLEAN DEFAULT 0,
                FOREIGN KEY (tortoise_id) REFERENCES tortoises(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Feeding items (what was fed in each feeding session)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feeding_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feeding_record_id INTEGER NOT NULL,
                plant_id INTEGER,
                supplement_name TEXT,
                weight REAL NOT NULL,
                notes TEXT,
                FOREIGN KEY (feeding_record_id) REFERENCES feeding_records(id),
                FOREIGN KEY (plant_id) REFERENCES plants(id)
            )
        ''')
        
        # Health records
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tortoise_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                record_type TEXT CHECK(record_type IN ('vet_visit', 'observation', 'medication', 'injury', 'behavior')),
                title TEXT NOT NULL,
                description TEXT,
                vet_name TEXT,
                diagnosis TEXT,
                treatment TEXT,
                medication TEXT,
                follow_up_date DATE,
                photo_path TEXT,
                priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
                resolved BOOLEAN DEFAULT 0,
                FOREIGN KEY (tortoise_id) REFERENCES tortoises(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Growth records
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS growth_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tortoise_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                measurement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                weight REAL,
                length REAL,
                width REAL,
                height REAL,
                photo_path TEXT,
                notes TEXT,
                FOREIGN KEY (tortoise_id) REFERENCES tortoises(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Habitat monitoring (for Adafruit.IO data)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habitat_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                temperature REAL,
                humidity REAL,
                basking_temp REAL,
                cool_temp REAL,
                uv_index REAL,
                alert_triggered BOOLEAN DEFAULT 0,
                alert_type TEXT
            )
        ''')
        
        # Care reminders and tasks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS care_reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                assigned_user_id INTEGER,
                tortoise_id INTEGER,
                reminder_type TEXT CHECK(reminder_type IN ('daily', 'weekly', 'monthly', 'yearly', 'once')),
                frequency_days INTEGER DEFAULT 1,
                next_due_date TIMESTAMP,
                last_completed TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                priority TEXT CHECK(priority IN ('low', 'medium', 'high')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assigned_user_id) REFERENCES users(id),
                FOREIGN KEY (tortoise_id) REFERENCES tortoises(id)
            )
        ''')
        
        # Settings for Adafruit.IO and other configurations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default settings
        default_settings = [
            ('adafruit_io_key', '', 'Adafruit.IO API Key'),
            ('adafruit_io_username', '', 'Adafruit.IO Username'),
            ('temp_feed_name', 'temperature', 'Temperature feed name'),
            ('humidity_feed_name', 'humidity', 'Humidity feed name'),
            ('temp_min', '20', 'Minimum temperature (°C)'),
            ('temp_max', '35', 'Maximum temperature (°C)'),
            ('humidity_min', '60', 'Minimum humidity (%)'),
            ('humidity_max', '80', 'Maximum humidity (%)'),
            ('photo_import_folder', '/home/pi/tortoise_photos', 'Folder to watch for new photos'),
        ]
        
        for key, value, description in default_settings:
            cursor.execute('''
                INSERT OR IGNORE INTO settings (key, value, description) 
                VALUES (?, ?, ?)
            ''', (key, value, description))
        
        # Insert default Hermann's tortoise safe plants
        default_plants = [
            ('Dandelion', 'Taraxacum officinale', 'safe', 'High in calcium, good for shell health', 'daily'),
            ('Plantain', 'Plantago major', 'safe', 'Good source of fiber', '2-3 times per week'),
            ('Clover', 'Trifolium species', 'safe', 'High protein content', '2-3 times per week'),
            ('Rose petals', 'Rosa species', 'safe', 'Vitamin C, occasional treat', 'weekly'),
            ('Hibiscus flowers', 'Hibiscus rosa-sinensis', 'safe', 'High in vitamin C', 'weekly'),
            ('Mulberry leaves', 'Morus species', 'safe', 'Excellent nutrition', 'daily'),
            ('Grape leaves', 'Vitis vinifera', 'safe', 'Good occasional food', '2-3 times per week'),
            ('Chickweed', 'Stellaria media', 'safe', 'Good winter green', 'daily'),
            ('Bramble leaves', 'Rubus species', 'safe', 'Blackberry/raspberry leaves', '2-3 times per week'),
            ('Mallow', 'Malva species', 'safe', 'Good source of mucilage', '2-3 times per week')
        ]
        
        for name, scientific, safety, nutrition, frequency in default_plants:
            cursor.execute('''
                INSERT OR IGNORE INTO plants (name, scientific_name, safety_level, nutrition_notes, feeding_frequency) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, scientific, safety, nutrition, frequency))
        
        # Insert default user if none exist
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', ('Default User', ''))
        
        conn.commit()
        print("Database initialized successfully!")
    
    def get_setting(self, key: str) -> Optional[str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        return result['value'] if result else None
    
    def set_setting(self, key: str, value: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at) 
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        conn.commit()
    
    def add_user(self, name: str, email: str = '') -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        return cursor.lastrowid
    
    def get_users(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
    
    def add_tortoise(self, name: str, species: str = "Hermann's Tortoise", **kwargs) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tortoises (name, species, subspecies, sex, birth_date, acquisition_date, current_weight, notes, photo_path) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, species, kwargs.get('subspecies'), kwargs.get('sex'), 
              kwargs.get('birth_date'), kwargs.get('acquisition_date'),
              kwargs.get('current_weight'), kwargs.get('notes'), kwargs.get('photo_path')))
        conn.commit()
        return cursor.lastrowid
    
    def get_tortoises(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tortoises WHERE is_active = 1 ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
    
    def get_plants(self, safety_level: Optional[str] = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if safety_level:
            cursor.execute('SELECT * FROM plants WHERE safety_level = ? ORDER BY name', (safety_level,))
        else:
            cursor.execute('SELECT * FROM plants ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]