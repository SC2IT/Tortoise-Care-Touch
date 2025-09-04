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
                role TEXT DEFAULT 'Caregiver',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add role column if it doesn't exist (for existing databases)
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN role TEXT DEFAULT "Caregiver"')
        except sqlite3.OperationalError:
            pass  # Column already exists
            
        # Add physical_description column if it doesn't exist
        try:
            cursor.execute('ALTER TABLE tortoises ADD COLUMN physical_description TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
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
                physical_description TEXT,
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
        
        # Insert comprehensive tortoise plant database
        default_plants = [
            # Daily safe foods - Feed freely
            ('Dandelion', 'Taraxacum officinale', 'safe', 'High in calcium and vitamin A, excellent for shell health', 'daily'),
            ('Plantain', 'Plantago major', 'safe', 'High fiber, good for digestive health', 'daily'),
            ('Chickweed', 'Stellaria media', 'safe', 'Good winter green, high in vitamins', 'daily'),
            ('Mallow', 'Malva species', 'safe', 'High in mucilage, good for digestion', 'daily'),
            ('Sow thistle', 'Sonchus species', 'safe', 'High calcium, similar to dandelion', 'daily'),
            ('Prickly pear cactus', 'Opuntia species', 'safe', 'High water content, good in hot weather', 'daily'),
            ('Lambs lettuce', 'Valerianella locusta', 'safe', 'Mild flavor, good vitamin content', 'daily'),
            ('Wild rocket', 'Diplotaxis tenuifolia', 'safe', 'Peppery flavor, high in calcium', 'daily'),
            
            # Weeds and wild plants - Safe daily
            ('Cleavers', 'Galium aparine', 'safe', 'Good source of chlorophyll', 'daily'),
            ('Goose grass', 'Galium aparine', 'safe', 'High in vitamins A and C', 'daily'),
            ('White dead nettle', 'Lamium album', 'safe', 'Good source of calcium', 'daily'),
            ('Cats ear', 'Hypochaeris radicata', 'safe', 'Similar to dandelion', 'daily'),
            ('Shepherds purse', 'Capsella bursa-pastoris', 'safe', 'High in vitamin K', 'daily'),
            ('Ribwort plantain', 'Plantago lanceolata', 'safe', 'Natural antibiotic properties', 'daily'),
            
            # Trees and shrubs - Safe moderation
            ('Mulberry leaves', 'Morus species', 'safe', 'Excellent nutrition, very palatable', '2-3 times per week'),
            ('Grape leaves', 'Vitis vinifera', 'safe', 'Good occasional food, not too much', '2-3 times per week'),
            ('Bramble leaves', 'Rubus species', 'safe', 'Blackberry/raspberry leaves', '2-3 times per week'),
            ('Rose leaves', 'Rosa species', 'safe', 'Good roughage, thorns removed', '2-3 times per week'),
            ('Apple leaves', 'Malus domestica', 'safe', 'Good fiber, avoid wilted leaves', '2-3 times per week'),
            ('Linden leaves', 'Tilia species', 'safe', 'Pleasant taste, good nutrition', '2-3 times per week'),
            ('Hazel leaves', 'Corylus avellana', 'safe', 'Good source of tannins', '2-3 times per week'),
            
            # Flowers - Safe treats
            ('Hibiscus flowers', 'Hibiscus rosa-sinensis', 'safe', 'High in vitamin C, colorful', 'weekly'),
            ('Rose petals', 'Rosa species', 'safe', 'Vitamin C, remove thorns', 'weekly'),
            ('Nasturtium flowers', 'Tropaeolum majus', 'safe', 'Peppery flavor, high in vitamin C', 'weekly'),
            ('Pansy', 'Viola tricolor', 'safe', 'Edible flowers, mild flavor', 'weekly'),
            ('Calendula', 'Calendula officinalis', 'safe', 'Anti-inflammatory properties', 'weekly'),
            ('Sunflower petals', 'Helianthus annuus', 'safe', 'Remove seeds, petals only', 'weekly'),
            ('Geranium flowers', 'Pelargonium species', 'safe', 'Colorful treat, mild flavor', 'weekly'),
            
            # Vegetables and cultivated plants - Moderation
            ('Rocket salad', 'Eruca sativa', 'safe', 'Peppery flavor, high calcium', '2-3 times per week'),
            ('Watercress', 'Nasturtium officinale', 'safe', 'High in vitamins, peppery taste', '2-3 times per week'),
            ('Endive', 'Cichorium endivia', 'safe', 'Good source of fiber and vitamins', '2-3 times per week'),
            ('Radicchio', 'Cichorium intybus', 'safe', 'Bitter flavor, good for liver', '2-3 times per week'),
            ('Mustard greens', 'Brassica juncea', 'caution', 'High in goitrogens, feed sparingly', 'weekly'),
            ('Kale', 'Brassica oleracea', 'caution', 'High in goitrogens and oxalates', 'weekly'),
            ('Collard greens', 'Brassica oleracea', 'caution', 'High calcium but also goitrogens', 'weekly'),
            
            # Herbs - Safe in moderation
            ('Thyme', 'Thymus vulgaris', 'safe', 'Antiseptic properties, strong flavor', 'weekly'),
            ('Oregano', 'Origanum vulgare', 'safe', 'Antibiotic properties, use sparingly', 'weekly'),
            ('Sage', 'Salvia officinalis', 'safe', 'Strong flavor, digestive aid', 'weekly'),
            ('Basil', 'Ocimum basilicum', 'safe', 'Aromatic herb, occasional treat', 'weekly'),
            ('Parsley', 'Petroselinum crispum', 'caution', 'High in oxalates, occasional only', 'monthly'),
            
            # Grasses and cereals
            ('Timothy grass', 'Phleum pratense', 'safe', 'Good fiber source', 'daily'),
            ('Meadow grass', 'Poa species', 'safe', 'Natural grazing food', 'daily'),
            ('Oat grass', 'Avena sativa', 'safe', 'Good when young and tender', 'daily'),
            
            # Fruits - Treats only
            ('Apple', 'Malus domestica', 'safe', 'Remove seeds, occasional treat', 'weekly'),
            ('Pear', 'Pyrus communis', 'safe', 'Remove seeds, high water content', 'weekly'),
            ('Strawberry', 'Fragaria species', 'safe', 'Including leaves, occasional treat', 'weekly'),
            ('Melon', 'Cucumis melo', 'safe', 'High water content, summer treat', 'weekly'),
            ('Fig', 'Ficus carica', 'safe', 'High sugar, very occasional', 'monthly'),
            
            # Potentially problematic - Caution
            ('Spinach', 'Spinacia oleracea', 'caution', 'Very high in oxalates', 'monthly'),
            ('Beet greens', 'Beta vulgaris', 'caution', 'High in oxalates', 'monthly'),
            ('Swiss chard', 'Beta vulgaris', 'caution', 'High in oxalates', 'monthly'),
            ('Rhubarb leaves', 'Rheum rhabarbarum', 'toxic', 'Contain oxalic acid, never feed', 'never'),
            
            # Common toxic plants - Never feed
            ('Buttercup', 'Ranunculus species', 'toxic', 'Contains ranunculin, causes blistering', 'never'),
            ('Foxglove', 'Digitalis purpurea', 'toxic', 'Contains digitoxin, affects heart', 'never'),
            ('Ivy', 'Hedera helix', 'toxic', 'Contains saponins, causes digestive issues', 'never'),
            ('Daffodil', 'Narcissus species', 'toxic', 'Contains alkaloids, very poisonous', 'never'),
            ('Azalea', 'Rhododendron species', 'toxic', 'Contains grayanotoxins', 'never'),
            ('Oleander', 'Nerium oleander', 'toxic', 'Extremely poisonous, affects heart', 'never'),
            ('Yew', 'Taxus baccata', 'toxic', 'Contains taxine, extremely dangerous', 'never'),
            ('Potato leaves', 'Solanum tuberosum', 'toxic', 'Contains solanine', 'never'),
            ('Tomato leaves', 'Solanum lycopersicum', 'toxic', 'Contains solanine', 'never'),
            ('Avocado', 'Persea americana', 'toxic', 'Contains persin, toxic to reptiles', 'never')
        ]
        
        # DISABLED: Default plants insertion - using single source of truth approach
        # for name, scientific, safety, nutrition, frequency in default_plants:
        #     cursor.execute('''
        #         INSERT OR IGNORE INTO plants (name, scientific_name, safety_level, nutrition_notes, feeding_frequency) 
        #         VALUES (?, ?, ?, ?, ?)
        #     ''', (name, scientific, safety, nutrition, frequency))
        
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
    
    def add_user(self, name: str, email: str = '', role: str = 'Caregiver') -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, role) VALUES (?, ?, ?)', (name, email, role))
        conn.commit()
        return cursor.lastrowid
    
    def get_users(self, include_inactive: bool = False) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if include_inactive:
            cursor.execute('SELECT * FROM users ORDER BY is_active DESC, name')
        else:
            cursor.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
    
    def update_user(self, user_id: int, name: str = None, email: str = None, role: str = None) -> bool:
        """Update user information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if name is not None:
            updates.append('name = ?')
            params.append(name)
        if email is not None:
            updates.append('email = ?')
            params.append(email)
        if role is not None:
            updates.append('role = ?')
            params.append(role)
        
        if not updates:
            return False
            
        params.append(user_id)
        query = f'UPDATE users SET {", ".join(updates)} WHERE id = ?'
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user (soft delete)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    def activate_user(self, user_id: int) -> bool:
        """Reactivate a deactivated user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_active = 1 WHERE id = ?', (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    def add_tortoise(self, name: str, species: str = "Hermann's Tortoise", **kwargs) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tortoises (name, species, subspecies, sex, birth_date, acquisition_date, current_weight, notes, physical_description, photo_path) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, species, kwargs.get('subspecies'), kwargs.get('sex'), 
              kwargs.get('birth_date'), kwargs.get('acquisition_date'),
              kwargs.get('current_weight'), kwargs.get('notes'), kwargs.get('physical_description'), kwargs.get('photo_path')))
        conn.commit()
        return cursor.lastrowid
    
    def get_tortoises(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tortoises WHERE is_active = 1 ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_tortoises(self) -> List[Dict]:
        """Get all active tortoises - alias for compatibility"""
        return self.get_tortoises()
    
    def get_tortoise_by_id(self, tortoise_id: int) -> Dict:
        """Get a single tortoise by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tortoises WHERE id = ? AND is_active = 1', (tortoise_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_tortoise_photo(self, tortoise_id: int, photo_path: str):
        """Update the photo path for a tortoise"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tortoises SET photo_path = ? WHERE id = ?', (photo_path, tortoise_id))
        conn.commit()
    
    def update_tortoise(self, tortoise_id: int, **kwargs):
        """Update tortoise information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        
        for field in ['name', 'species', 'subspecies', 'sex', 'birth_date', 
                     'acquisition_date', 'current_weight', 'notes', 'physical_description']:
            if field in kwargs:
                fields.append(f"{field} = ?")
                values.append(kwargs[field])
        
        if fields:
            query = f"UPDATE tortoises SET {', '.join(fields)} WHERE id = ?"
            values.append(tortoise_id)
            cursor.execute(query, values)
            conn.commit()
    
    def deactivate_tortoise(self, tortoise_id: int):
        """Deactivate a tortoise"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tortoises SET is_active = 0 WHERE id = ?', (tortoise_id,))
        conn.commit()
    
    def activate_tortoise(self, tortoise_id: int):
        """Activate a tortoise"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tortoises SET is_active = 1 WHERE id = ?', (tortoise_id,))
        conn.commit()
    
    def get_plants(self, safety_level: Optional[str] = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if safety_level:
            cursor.execute('SELECT * FROM plants WHERE safety_level = ? ORDER BY name', (safety_level,))
        else:
            cursor.execute('SELECT * FROM plants ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
    
    # Health Record Management Methods
    def add_health_record(self, tortoise_id: int, user_id: int, record_type: str, title: str, 
                         description: str = '', vet_name: str = '', diagnosis: str = '', 
                         treatment: str = '', medication: str = '', follow_up_date: str = '',
                         photo_path: str = '', priority: str = 'medium') -> int:
        """Add a new health record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO health_records (tortoise_id, user_id, record_type, title, description,
                                      vet_name, diagnosis, treatment, medication, follow_up_date,
                                      photo_path, priority) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tortoise_id, user_id, record_type, title, description, vet_name, diagnosis,
              treatment, medication, follow_up_date or None, photo_path, priority))
        conn.commit()
        return cursor.lastrowid
    
    def get_health_records(self, tortoise_id: Optional[int] = None, record_type: Optional[str] = None,
                          resolved: Optional[bool] = None) -> List[Dict]:
        """Get health records with optional filtering"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT hr.*, t.name as tortoise_name, u.name as user_name
            FROM health_records hr
            JOIN tortoises t ON hr.tortoise_id = t.id
            JOIN users u ON hr.user_id = u.id
            WHERE 1=1
        '''
        params = []
        
        if tortoise_id:
            query += ' AND hr.tortoise_id = ?'
            params.append(tortoise_id)
        if record_type:
            query += ' AND hr.record_type = ?'
            params.append(record_type)
        if resolved is not None:
            query += ' AND hr.resolved = ?'
            params.append(resolved)
            
        query += ' ORDER BY hr.record_date DESC'
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def update_health_record(self, record_id: int, **kwargs) -> bool:
        """Update health record fields"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        allowed_fields = ['title', 'description', 'vet_name', 'diagnosis', 'treatment', 
                         'medication', 'follow_up_date', 'photo_path', 'priority', 'resolved']
        
        updates = []
        params = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f'{field} = ?')
                params.append(value)
        
        if not updates:
            return False
            
        params.append(record_id)
        query = f'UPDATE health_records SET {", ".join(updates)} WHERE id = ?'
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    
    def get_health_record_by_id(self, record_id: int) -> Optional[Dict]:
        """Get a specific health record by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT hr.*, t.name as tortoise_name, u.name as user_name
            FROM health_records hr
            JOIN tortoises t ON hr.tortoise_id = t.id
            JOIN users u ON hr.user_id = u.id
            WHERE hr.id = ?
        ''', (record_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def delete_health_record(self, record_id: int) -> bool:
        """Delete a health record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM health_records WHERE id = ?', (record_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    def get_health_summary(self, tortoise_id: int) -> Dict:
        """Get health summary statistics for a tortoise"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get total records count
        cursor.execute('SELECT COUNT(*) as total FROM health_records WHERE tortoise_id = ?', (tortoise_id,))
        total_records = cursor.fetchone()[0]
        
        # Get unresolved issues count
        cursor.execute('SELECT COUNT(*) as unresolved FROM health_records WHERE tortoise_id = ? AND resolved = 0', (tortoise_id,))
        unresolved_issues = cursor.fetchone()[0]
        
        # Get recent records (last 30 days)
        cursor.execute('''
            SELECT COUNT(*) as recent FROM health_records 
            WHERE tortoise_id = ? AND record_date > datetime('now', '-30 days')
        ''', (tortoise_id,))
        recent_records = cursor.fetchone()[0]
        
        # Get urgent issues
        cursor.execute('SELECT COUNT(*) as urgent FROM health_records WHERE tortoise_id = ? AND priority = "urgent" AND resolved = 0', (tortoise_id,))
        urgent_issues = cursor.fetchone()[0]
        
        return {
            'total_records': total_records,
            'unresolved_issues': unresolved_issues,
            'recent_records': recent_records,
            'urgent_issues': urgent_issues
        }
    
    # Settings Management Methods
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value by key"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        return row[0] if row else None
    
    def set_setting(self, key: str, value: str, description: str = '') -> bool:
        """Set a setting value"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, description, updated_at) 
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (key, value, description))
        conn.commit()
        return True
    
    def get_all_settings(self) -> Dict[str, str]:
        """Get all settings as a dictionary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT key, value FROM settings')
        return {row[0]: row[1] for row in cursor.fetchall()}