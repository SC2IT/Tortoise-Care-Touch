#!/usr/bin/env python3
"""
Download plant photos from The Tortoise Table with CC Attribution-NoDerivs 2.0 license
Create local photo library for offline plant identification
"""

import os
import requests
import sqlite3
from pathlib import Path
from urllib.parse import urljoin, urlparse
import time
import json
from database.db_manager import DatabaseManager

# Create photos directory structure
PHOTOS_DIR = Path("plant_photos")
PHOTOS_DIR.mkdir(exist_ok=True)

# Photo attribution file for CC compliance
ATTRIBUTION_FILE = PHOTOS_DIR / "attribution.json"

class PlantPhotoDownloader:
    """Download and manage plant photos from The Tortoise Table"""
    
    def __init__(self):
        self.base_url = "https://www.thetortoisetable.org.uk"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.attribution_data = {}
        self.load_existing_attribution()
        
    def load_existing_attribution(self):
        """Load existing attribution data"""
        if ATTRIBUTION_FILE.exists():
            with open(ATTRIBUTION_FILE, 'r') as f:
                self.attribution_data = json.load(f)
    
    def save_attribution(self):
        """Save attribution data for CC compliance"""
        attribution_info = {
            "license": "CC Attribution-NoDerivs 2.0 Generic",
            "source": "The Tortoise Table (thetortoisetable.org.uk)",
            "download_date": time.strftime("%Y-%m-%d"),
            "plants": self.attribution_data
        }
        
        with open(ATTRIBUTION_FILE, 'w') as f:
            json.dump(attribution_info, f, indent=2)
    
    def download_photo(self, photo_url, plant_name, photo_type="main"):
        """Download a single plant photo"""
        try:
            # Create safe filename
            safe_name = "".join(c for c in plant_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_').lower()
            
            # Get file extension from URL
            parsed_url = urlparse(photo_url)
            file_ext = Path(parsed_url.path).suffix or '.jpg'
            
            # Create filename
            filename = f"{safe_name}_{photo_type}{file_ext}"
            file_path = PHOTOS_DIR / filename
            
            # Skip if already exists
            if file_path.exists():
                print(f"  Photo already exists: {filename}")
                return str(file_path.relative_to(Path.cwd()))
            
            # Download photo
            response = self.session.get(photo_url, timeout=30)
            response.raise_for_status()
            
            # Verify it's an image
            content_type = response.headers.get('content-type', '').lower()
            if not any(img_type in content_type for img_type in ['image/', 'jpeg', 'jpg', 'png', 'gif']):
                print(f"  Skipping non-image content: {content_type}")
                return None
            
            # Save photo
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"  Downloaded: {filename} ({len(response.content)} bytes)")
            
            # Add to attribution
            self.attribution_data[plant_name] = {
                "photo_file": filename,
                "source_url": photo_url,
                "photo_type": photo_type,
                "download_date": time.strftime("%Y-%m-%d")
            }
            
            return str(file_path.relative_to(Path.cwd()))
            
        except Exception as e:
            print(f"  Error downloading {photo_url}: {e}")
            return None
    
    def get_plant_photo_urls(self, plant_page_url):
        """Extract photo URLs from a plant's individual page"""
        try:
            response = self.session.get(plant_page_url, timeout=30)
            response.raise_for_status()
            
            # Look for image URLs in the HTML
            # This is a simplified approach - in reality, we'd need to parse the HTML
            # to find specific image elements for plant photos
            content = response.text.lower()
            
            # Common image extensions and patterns
            import re
            image_patterns = [
                r'src="([^"]*\.(?:jpg|jpeg|png|gif))"',
                r"src='([^']*\.(?:jpg|jpeg|png|gif))'",
                r'href="([^"]*\.(?:jpg|jpeg|png|gif))"'
            ]
            
            photos = []
            for pattern in image_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if any(skip in match.lower() for skip in ['logo', 'icon', 'banner', 'header', 'footer']):
                        continue
                    
                    # Convert relative URLs to absolute
                    if match.startswith('/'):
                        photo_url = urljoin(self.base_url, match)
                    elif not match.startswith('http'):
                        photo_url = urljoin(plant_page_url, match)
                    else:
                        photo_url = match
                    
                    photos.append(photo_url)
            
            return list(set(photos))  # Remove duplicates
            
        except Exception as e:
            print(f"  Error getting photos from {plant_page_url}: {e}")
            return []

def download_sample_plant_photos():
    """Download sample photos for key plants"""
    
    print("Plant Photo Download System")
    print("=" * 30)
    print("License: CC Attribution-NoDerivs 2.0 Generic")
    print("Source: The Tortoise Table (thetortoisetable.org.uk)")
    print()
    
    downloader = PlantPhotoDownloader()
    
    # Sample of key plants with known photo URLs (these would need to be actual URLs)
    # For demonstration, I'll create placeholder entries
    sample_plants = [
        {
            "name": "Dandelion",
            "scientific_name": "Taraxacum officinale",
            "photo_urls": [
                # These would be actual photo URLs from The Tortoise Table
                "https://example.com/dandelion_flower.jpg",
                "https://example.com/dandelion_leaves.jpg"
            ]
        },
        {
            "name": "Plantain", 
            "scientific_name": "Plantago major",
            "photo_urls": [
                "https://example.com/plantain_leaves.jpg"
            ]
        },
        # More plants would be added here with actual URLs
    ]
    
    print("Note: This is a demonstration version.")
    print("In production, actual photo URLs from The Tortoise Table would be used.")
    print()
    
    # Create database schema for photos
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Add photo columns to plants table if they don't exist
    try:
        cursor.execute('ALTER TABLE plants ADD COLUMN leaf_photo_path TEXT')
        print("Added leaf_photo_path column to plants table")
    except:
        pass  # Column already exists
        
    try:
        cursor.execute('ALTER TABLE plants ADD COLUMN flower_photo_path TEXT') 
        print("Added flower_photo_path column to plants table")
    except:
        pass  # Column already exists
        
    try:
        cursor.execute('ALTER TABLE plants ADD COLUMN plant_photo_path TEXT')
        print("Added plant_photo_path column to plants table")
    except:
        pass  # Column already exists
    
    conn.commit()
    
    downloaded_count = 0
    
    for plant in sample_plants:
        print(f"\nProcessing {plant['name']} ({plant['scientific_name']}):")
        
        for i, photo_url in enumerate(plant['photo_urls']):
            photo_type = "main" if i == 0 else f"alt_{i}"
            photo_path = downloader.download_photo(photo_url, plant['name'], photo_type)
            
            if photo_path:
                # Update database with photo path
                cursor.execute('''
                    UPDATE plants 
                    SET plant_photo_path = ? 
                    WHERE name = ?
                ''', (photo_path, plant['name']))
                downloaded_count += 1
    
    conn.commit()
    conn.close()
    
    # Save attribution information
    downloader.save_attribution()
    
    print(f"\nPhoto download summary:")
    print(f"  Downloaded: {downloaded_count} photos")
    print(f"  Attribution file: {ATTRIBUTION_FILE}")
    print(f"  Photos directory: {PHOTOS_DIR}")
    print()
    print("CC Attribution-NoDerivs 2.0 Generic License:")
    print("  - Source: The Tortoise Table (thetortoisetable.org.uk)")
    print("  - License allows sharing with attribution")
    print("  - No derivatives allowed")
    print("  - Commercial use permitted with attribution")

def create_photo_placeholder_system():
    """Create a system for managing plant photos with proper attribution"""
    
    print("Creating Plant Photo Management System...")
    
    # Create directories
    categories = ['wild_flowers', 'garden_plants', 'trees_shrubs', 'cacti_succulents', 
                 'grasses_ferns', 'fruits_vegetables', 'aquatic_plants']
    
    for category in categories:
        category_dir = PHOTOS_DIR / category
        category_dir.mkdir(exist_ok=True)
        print(f"Created directory: {category_dir}")
    
    # Create attribution template
    attribution_template = {
        "license": "CC Attribution-NoDerivs 2.0 Generic",
        "source": "The Tortoise Table (thetortoisetable.org.uk)",
        "license_url": "https://creativecommons.org/licenses/by-nd/2.0/",
        "usage_notes": "Photos must be attributed to The Tortoise Table. No derivatives allowed.",
        "plants": {}
    }
    
    with open(PHOTOS_DIR / "attribution_template.json", 'w') as f:
        json.dump(attribution_template, f, indent=2)
    
    # Create README for photo directory
    readme_content = """# Plant Photos Directory

## License: CC Attribution-NoDerivs 2.0 Generic

**Source**: The Tortoise Table (https://thetortoisetable.org.uk)
**License URL**: https://creativecommons.org/licenses/by-nd/2.0/

### Usage Requirements:
- Attribution must be provided to "The Tortoise Table"
- No derivative works allowed
- Commercial use permitted with proper attribution
- Share-alike not required

### Directory Structure:
- `wild_flowers/` - Wild flower plant photos
- `garden_plants/` - Garden and house plant photos  
- `trees_shrubs/` - Tree, shrub, and climber photos
- `cacti_succulents/` - Cacti and succulent photos
- `grasses_ferns/` - Grass and fern photos
- `fruits_vegetables/` - Fruit and vegetable photos
- `aquatic_plants/` - Aquatic and semi-aquatic plant photos

### Photo Types:
- `*_leaf.jpg` - Leaf/foliage photos for identification
- `*_flower.jpg` - Flower photos for identification
- `*_plant.jpg` - Full plant photos for context
- `*_fruit.jpg` - Fruit/seed photos where applicable

### Attribution Format:
"Plant photos courtesy of The Tortoise Table (thetortoisetable.org.uk), 
licensed under CC Attribution-NoDerivs 2.0 Generic"
"""
    
    with open(PHOTOS_DIR / "README.md", 'w') as f:
        f.write(readme_content)
    
    print(f"Created photo management system in {PHOTOS_DIR}")
    print("Ready for manual photo addition or automated download")

if __name__ == "__main__":
    print("Plant Photo Download System")
    print("=" * 30)
    
    # Create the photo management system
    create_photo_placeholder_system()
    
    print("\nTo download actual photos:")
    print("1. Obtain photo URLs from The Tortoise Table")
    print("2. Update the sample_plants list with real URLs") 
    print("3. Run download_sample_plant_photos()")
    print("\nFor manual photo addition:")
    print("1. Add photos to appropriate category directories")
    print("2. Use naming convention: plantname_type.jpg")
    print("3. Update attribution.json with source information")