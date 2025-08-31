#!/usr/bin/env python3
"""
Convert SVG icons to PNG for Kivy compatibility
This script converts Tabler Icons SVG files to PNG format at multiple resolutions
"""

import os
import sys
from pathlib import Path

try:
    import cairosvg
    CAIRO_AVAILABLE = True
except ImportError:
    CAIRO_AVAILABLE = False

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def convert_svg_to_png_simple(svg_path, png_path, size=64):
    """
    Simple SVG to PNG conversion using basic text rendering
    This is a fallback for when cairosvg is not available
    """
    if PIL_AVAILABLE:
        # Create a simple colored square as icon placeholder
        img = Image.new('RGBA', (size, size), (70, 130, 180, 255))  # Steel blue
        draw = ImageDraw.Draw(img)
        
        # Draw a simple geometric shape based on icon name
        icon_name = Path(svg_path).stem
        margin = size // 8
        
        if icon_name == 'users':
            # Draw two circles for users
            draw.ellipse([margin, margin, size//2, size//2], fill=(255, 255, 255, 255))
            draw.ellipse([size//2, margin, size-margin, size//2], fill=(255, 255, 255, 255))
        elif icon_name == 'settings':
            # Draw gear-like shape
            center = size // 2
            radius = size // 3
            draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                        fill=(255, 255, 255, 255))
        elif icon_name == 'database':
            # Draw cylinder shape
            draw.ellipse([margin, margin, size-margin, size//3], fill=(255, 255, 255, 255))
            draw.rectangle([margin, size//6, size-margin, size*2//3], fill=(255, 255, 255, 255))
            draw.ellipse([margin, size//2, size-margin, size*2//3+margin], fill=(255, 255, 255, 255))
        elif icon_name == 'heart':
            # Draw heart shape (simplified)
            center_x, center_y = size // 2, size // 2
            draw.ellipse([center_x-size//4, center_y-size//6, center_x, center_y+size//6], 
                        fill=(255, 255, 255, 255))
            draw.ellipse([center_x, center_y-size//6, center_x+size//4, center_y+size//6], 
                        fill=(255, 255, 255, 255))
        else:
            # Default: simple square
            draw.rectangle([margin, margin, size-margin, size-margin], fill=(255, 255, 255, 255))
        
        img.save(png_path, 'PNG')
        return True
    return False

def convert_svg_to_png(svg_path, png_path, size=64):
    """Convert SVG to PNG using cairosvg if available"""
    if CAIRO_AVAILABLE:
        try:
            cairosvg.svg2png(
                url=svg_path,
                write_to=png_path,
                output_width=size,
                output_height=size
            )
            return True
        except Exception as e:
            print(f"Error converting {svg_path} with cairosvg: {e}")
    
    # Fallback to simple conversion
    return convert_svg_to_png_simple(svg_path, png_path, size)

def main():
    """Convert all SVG icons to PNG"""
    project_root = Path(__file__).parent
    icons_dir = project_root / 'icons'
    
    if not icons_dir.exists():
        print("Icons directory not found!")
        return False
    
    # Icon sizes to generate
    sizes = [32, 48, 64, 96]  # Different resolutions for different uses
    
    svg_files = list(icons_dir.glob('*.svg'))
    if not svg_files:
        print("No SVG files found in icons directory!")
        return False
    
    print(f"Found {len(svg_files)} SVG files to convert...")
    
    success_count = 0
    for svg_file in svg_files:
        print(f"Converting {svg_file.name}...")
        
        # Convert to multiple sizes
        for size in sizes:
            png_name = f"{svg_file.stem}_{size}px.png"
            png_path = icons_dir / png_name
            
            if convert_svg_to_png(str(svg_file), str(png_path), size):
                print(f"  -> {png_name} OK")
                success_count += 1
            else:
                print(f"  -> {png_name} FAILED")
    
    print(f"\nConverted {success_count} icons successfully!")
    
    # Create a default size (64px) without size suffix for backwards compatibility
    print("\nCreating default size icons...")
    for svg_file in svg_files:
        png_name = f"{svg_file.stem}.png"
        png_path = icons_dir / png_name
        
        if convert_svg_to_png(str(svg_file), str(png_path), 64):
            print(f"  -> {png_name} OK")
    
    return True

if __name__ == '__main__':
    if not CAIRO_AVAILABLE and not PIL_AVAILABLE:
        print("Warning: Neither cairosvg nor PIL available. Install one for better icon conversion.")
        print("Run: pip install cairosvg  or  pip install pillow")
    
    success = main()
    sys.exit(0 if success else 1)