#!/usr/bin/env python3
"""
Download real plant photos from The Tortoise Table with CC Attribution-NoDerivs 2.0 license
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
from bs4 import BeautifulSoup
import re

# Create photos directory structure
PHOTOS_DIR = Path("plant_photos")
PHOTOS_DIR.mkdir(exist_ok=True)

# Photo attribution file for CC compliance
ATTRIBUTION_FILE = PHOTOS_DIR / "attribution.json"

class RealPlantPhotoDownloader:
    """Download and manage real plant photos from The Tortoise Table"""
    
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
            "license_url": "https://creativecommons.org/licenses/by-nd/2.0/",
            "source": "The Tortoise Table (thetortoisetable.org.uk)",
            "download_date": time.strftime("%Y-%m-%d"),
            "usage_notes": "Photos must be attributed to The Tortoise Table. No derivatives allowed.",
            "plants": self.attribution_data
        }
        
        with open(ATTRIBUTION_FILE, 'w') as f:
            json.dump(attribution_info, f, indent=2)
    
    def search_plant_on_tortoise_table(self, plant_name, scientific_name=None):
        """Search for a plant on The Tortoise Table and return the plant page URL"""
        try:
            search_url = f"{self.base_url}/plant-database/"
            response = self.session.get(search_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for plant links in the database
            plant_links = soup.find_all('a', href=True)
            
            for link in plant_links:
                link_text = link.get_text().lower().strip()
                href = link.get('href')
                
                # Check if link contains plant name or scientific name
                if (plant_name.lower() in link_text or 
                    (scientific_name and scientific_name.lower() in link_text) or
                    any(word in link_text for word in plant_name.lower().split())):
                    
                    if '/plants/' in href or '/plant/' in href:
                        full_url = urljoin(self.base_url, href)
                        print(f"  Found potential match: {link_text} -> {full_url}")
                        return full_url
            
            return None
            
        except Exception as e:
            print(f"  Error searching for {plant_name}: {e}")
            return None
    
    def extract_photos_from_plant_page(self, plant_url):
        """Extract photo URLs from a plant's individual page"""
        try:
            response = self.session.get(plant_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            photos = []
            
            # Look for images in various common containers
            img_tags = soup.find_all('img', src=True)
            
            for img in img_tags:
                src = img.get('src')
                alt = img.get('alt', '').lower()
                
                # Skip obvious non-plant images
                if any(skip in alt for skip in ['logo', 'icon', 'banner', 'header', 'footer', 'nav']):
                    continue
                    
                # Skip very small images (likely icons)
                width = img.get('width')
                height = img.get('height')
                if width and height:
                    try:
                        if int(width) < 50 or int(height) < 50:
                            continue
                    except:
                        pass
                
                # Convert relative URLs to absolute
                if src.startswith('/'):
                    photo_url = urljoin(self.base_url, src)
                elif not src.startswith('http'):
                    photo_url = urljoin(plant_url, src)
                else:
                    photo_url = src
                
                # Check if it's a valid image URL
                if any(ext in photo_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    photos.append(photo_url)
            
            return list(set(photos))  # Remove duplicates
            
        except Exception as e:
            print(f"  Error extracting photos from {plant_url}: {e}")
            return []
    
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
                print(f"    Photo already exists: {filename}")
                return str(file_path.relative_to(Path.cwd()))
            
            # Download photo
            response = self.session.get(photo_url, timeout=30)
            response.raise_for_status()
            
            # Verify it's an image
            content_type = response.headers.get('content-type', '').lower()
            if not any(img_type in content_type for img_type in ['image/', 'jpeg', 'jpg', 'png', 'gif']):
                print(f"    Skipping non-image content: {content_type}")
                return None
            
            # Save photo
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"    Downloaded: {filename} ({len(response.content)} bytes)")
            
            # Add to attribution
            if plant_name not in self.attribution_data:
                self.attribution_data[plant_name] = {}
            
            self.attribution_data[plant_name][photo_type] = {
                "photo_file": filename,
                "source_url": photo_url,
                "download_date": time.strftime("%Y-%m-%d")
            }
            
            return str(file_path.relative_to(Path.cwd()))
            
        except Exception as e:
            print(f"    Error downloading {photo_url}: {e}")
            return None

def download_photos_for_database_plants():
    """Download photos for all plants in our database"""
    
    print("Real Plant Photo Download System")
    print("=" * 40)
    print("License: CC Attribution-NoDerivs 2.0 Generic")
    print("Source: The Tortoise Table (thetortoisetable.org.uk)")
    print()
    
    downloader = RealPlantPhotoDownloader()
    
    # Get all plants from our database
    db = DatabaseManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, scientific_name, safety_level FROM plants ORDER BY name')
    plants = cursor.fetchall()
    
    print(f"Found {len(plants)} plants in database")
    print()
    
    # Add photo columns to plants table if they don't exist
    try:
        cursor.execute('ALTER TABLE plants ADD COLUMN main_photo_path TEXT')
        print("Added main_photo_path column to plants table")
    except:
        pass  # Column already exists
    
    conn.commit()
    
    downloaded_count = 0
    failed_count = 0
    
    for plant_id, name, scientific_name, safety_level in plants:
        print(f"Processing {name} ({scientific_name or 'no scientific name'}):")
        
        # Search for the plant on The Tortoise Table
        plant_url = downloader.search_plant_on_tortoise_table(name, scientific_name)
        
        if not plant_url:
            print(f"  Could not find {name} on The Tortoise Table")
            failed_count += 1
            time.sleep(1)  # Be nice to the server
            continue
        
        # Extract photos from the plant page
        photo_urls = downloader.extract_photos_from_plant_page(plant_url)
        
        if not photo_urls:
            print(f"  No photos found for {name}")
            failed_count += 1
            time.sleep(1)
            continue
        
        print(f"  Found {len(photo_urls)} potential photos")
        
        # Download the first/best photo
        photo_path = None
        for i, photo_url in enumerate(photo_urls[:3]):  # Try first 3 photos
            photo_type = "main" if i == 0 else f"alt_{i}"
            photo_path = downloader.download_photo(photo_url, name, photo_type)
            
            if photo_path and i == 0:  # Use first successful download as main photo
                # Update database with photo path
                cursor.execute('''
                    UPDATE plants 
                    SET main_photo_path = ? 
                    WHERE id = ?
                ''', (photo_path, plant_id))
                downloaded_count += 1
                break
        
        if not photo_path:
            print(f"  Failed to download any photos for {name}")
            failed_count += 1
        
        time.sleep(2)  # Be nice to the server
    
    conn.commit()
    conn.close()
    
    # Save attribution information
    downloader.save_attribution()
    
    print(f"\nPhoto download summary:")
    print(f"  Total plants: {len(plants)}")
    print(f"  Successfully downloaded: {downloaded_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Attribution file: {ATTRIBUTION_FILE}")
    print(f"  Photos directory: {PHOTOS_DIR}")
    print()
    print("CC Attribution-NoDerivs 2.0 Generic License:")
    print("  - Source: The Tortoise Table (thetortoisetable.org.uk)")
    print("  - License allows sharing with attribution")
    print("  - No derivatives allowed")
    print("  - Commercial use permitted with attribution")

if __name__ == "__main__":
    print("Real Plant Photo Download System")
    print("=" * 40)
    
    try:
        download_photos_for_database_plants()
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
    except Exception as e:
        print(f"\nError during download: {e}")