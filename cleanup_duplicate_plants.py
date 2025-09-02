#!/usr/bin/env python3
"""
Clean up duplicate plants in the database
Keeps the first entry of each unique plant name and removes duplicates
"""

import sqlite3
from database.db_manager import DatabaseManager

def cleanup_duplicate_plants():
    """Remove duplicate plants, keeping only one copy of each unique plant"""
    
    print("Cleaning up duplicate plants in database...")
    
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Get initial count
        cursor.execute('SELECT COUNT(*) FROM plants')
        initial_count = cursor.fetchone()[0]
        print(f"Initial plant count: {initial_count}")
        
        # Backup the original data (optional but recommended)
        print("Creating backup of plants table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plants_backup AS 
            SELECT * FROM plants
        ''')
        
        # Get unique plants (keep the one with lowest ID for each name)
        cursor.execute('''
            SELECT name, MIN(id) as keep_id, COUNT(*) as duplicate_count
            FROM plants 
            GROUP BY name
            HAVING COUNT(*) > 1
        ''')
        
        duplicates = cursor.fetchall()
        print(f"Found {len(duplicates)} plants with duplicates")
        
        # Delete duplicates (keep only the entry with minimum ID for each name)
        total_deleted = 0
        for name, keep_id, dup_count in duplicates:
            cursor.execute('''
                DELETE FROM plants 
                WHERE name = ? AND id > ?
            ''', (name, keep_id))
            deleted = cursor.rowcount
            total_deleted += deleted
            print(f"  {name}: kept ID {keep_id}, deleted {deleted} duplicates")
        
        # Get final count
        cursor.execute('SELECT COUNT(*) FROM plants')
        final_count = cursor.fetchone()[0]
        
        # Commit changes
        conn.commit()
        
        print(f"\nCleanup complete!")
        print(f"   Before: {initial_count} plants")
        print(f"   After:  {final_count} plants")
        print(f"   Deleted: {total_deleted} duplicates")
        print(f"   Unique plants preserved: {final_count}")
        
        # Show some examples of remaining plants
        print(f"\nSample of remaining plants:")
        cursor.execute('SELECT name, safety_level FROM plants ORDER BY name LIMIT 10')
        samples = cursor.fetchall()
        for name, safety in samples:
            print(f"  - {name} ({safety})")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"ERROR during cleanup: {e}")
        return False
    
    finally:
        conn.close()

def verify_cleanup():
    """Verify the cleanup was successful"""
    print(f"\nVerifying cleanup...")
    
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Check for any remaining duplicates
        cursor.execute('''
            SELECT name, COUNT(*) as count 
            FROM plants 
            GROUP BY name 
            HAVING count > 1
        ''')
        
        remaining_duplicates = cursor.fetchall()
        
        if remaining_duplicates:
            print(f"WARNING: Still found {len(remaining_duplicates)} duplicates:")
            for name, count in remaining_duplicates:
                print(f"   {name}: {count} entries")
        else:
            print("SUCCESS: No duplicates found - cleanup successful!")
            
        # Get final stats
        cursor.execute('SELECT COUNT(*) FROM plants')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT safety_level, COUNT(*) FROM plants GROUP BY safety_level')
        safety_stats = cursor.fetchall()
        
        print(f"\nFinal database stats:")
        print(f"  Total plants: {total}")
        for safety, count in safety_stats:
            print(f"  {safety.title()}: {count}")
            
    except Exception as e:
        print(f"ERROR during verification: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("Plant Database Cleanup Tool")
    print("=" * 40)
    
    # Ask for confirmation
    response = input("This will remove duplicate plants. Continue? (y/N): ").lower()
    
    if response == 'y':
        success = cleanup_duplicate_plants()
        if success:
            verify_cleanup()
    else:
        print("Cleanup cancelled.")