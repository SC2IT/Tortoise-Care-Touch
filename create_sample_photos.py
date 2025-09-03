#!/usr/bin/env python3
"""
Create sample placeholder photos for testing the photo display system
"""

import os
from pathlib import Path
from database.db_manager import DatabaseManager

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL (Pillow) not available. Installing...")

def install_pillow():
    """Install Pillow for image creation"""
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("Pillow installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install Pillow")
        return False

def create_placeholder_photo(plant_name, safety_level, filename):
    """Create a placeholder photo for a plant"""
    
    # Safety level colors
    colors = {
        'safe': (76, 175, 80),      # Green
        'caution': (255, 152, 0),   # Orange  
        'toxic': (244, 67, 54)      # Red
    }
    
    color = colors.get(safety_level, (76, 175, 80))
    
    # Create image
    width, height = 200, 200
    image = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(image)
    
    # Draw a simple plant-like shape (circle with stem)
    center_x, center_y = width // 2, height // 2 - 20
    
    # Draw "flower" (circle)
    flower_radius = 50
    flower_color = tuple(max(0, c - 50) for c in color)  # Darker shade
    draw.ellipse([center_x - flower_radius, center_y - flower_radius,
                  center_x + flower_radius, center_y + flower_radius], 
                 fill=flower_color, outline=(0, 0, 0), width=2)
    
    # Draw stem
    stem_width = 8
    stem_height = 60
    draw.rectangle([center_x - stem_width//2, center_y + flower_radius,
                    center_x + stem_width//2, center_y + flower_radius + stem_height],
                   fill=(0, 100, 0), outline=(0, 50, 0))
    
    # Add text
    try:
        # Try to use a default font
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    # Plant name (truncated if too long)
    display_name = plant_name[:15] + "..." if len(plant_name) > 15 else plant_name
    
    # Get text size for centering
    bbox = draw.textbbox((0, 0), display_name, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    
    # Draw text with outline for better readability
    outline_color = (255, 255, 255) if sum(color) < 384 else (0, 0, 0)
    text_color = (0, 0, 0) if sum(color) > 384 else (255, 255, 255)
    
    # Draw text outline
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                draw.text((text_x + dx, height - 30 + dy), display_name, 
                         font=font, fill=outline_color)
    
    # Draw main text
    draw.text((text_x, height - 30), display_name, font=font, fill=text_color)
    
    # Save image
    image.save(filename, "PNG")
    print(f"Created placeholder photo: {filename}")

def create_sample_photos_for_database():
    """Create placeholder photos for all plants in the database"""
    
    if not PIL_AVAILABLE:
        if not install_pillow():
            print("Cannot create photos without Pillow. Exiting.")
            return
        
        # Re-import after installation
        try:
            global Image, ImageDraw, ImageFont
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            print("Still cannot import Pillow. Please restart and try again.")
            return
    
    print("Creating sample placeholder photos...")
    
    # Create photos directory
    photos_dir = Path("plant_photos")
    photos_dir.mkdir(exist_ok=True)
    
    # Get all plants from database
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, safety_level FROM plants ORDER BY name')
    plants = cursor.fetchall()
    
    created_count = 0
    
    for plant_id, name, safety_level in plants:
        # Create safe filename
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_').lower()
        
        filename = photos_dir / f"{safe_name}_placeholder.png"
        
        # Skip if already exists
        if filename.exists():
            print(f"Photo already exists for {name}")
            continue
        
        try:
            create_placeholder_photo(name, safety_level, str(filename))
            
            # Update database with photo path
            relative_path = str(filename).replace('\\', '/')
            cursor.execute('''
                UPDATE plants 
                SET main_photo_path = ? 
                WHERE id = ?
            ''', (relative_path, plant_id))
            
            created_count += 1
            
        except Exception as e:
            print(f"Error creating photo for {name}: {e}")
    
    # Commit database changes
    conn.commit()
    conn.close()
    
    print(f"\nCreated {created_count} placeholder photos")
    print(f"Photos saved in: {photos_dir}")
    print("Database updated with photo paths")

if __name__ == "__main__":
    print("Plant Photo Creator")
    print("=" * 30)
    create_sample_photos_for_database()