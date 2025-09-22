#!/usr/bin/env python3
"""
Generate PWA icons from source logo
Requires: Pillow (PIL fork)
Install with: pip install Pillow
"""

import os
from PIL import Image

def generate_pwa_icons(source_path, output_dir, sizes=(192, 512)):
    """
    Generate PWA icons in different sizes from source image
    :param source_path: Path to source logo image
    :param output_dir: Directory to save generated icons
    :param sizes: Tuple of icon sizes to generate
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open and convert to RGBA to ensure transparency support
    with Image.open(source_path) as img:
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        # Generate icons for each size
        for size in sizes:
            # Create a white background image
            background = Image.new('RGBA', (size, size), (255, 255, 255, 255))
            
            # Calculate scaling to fit within the size while maintaining aspect ratio
            ratio = min(size/img.width, size/img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            resized = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Calculate position to center the image
            position = ((size - new_size[0]) // 2, (size - new_size[1]) // 2)
            
            # Paste resized image onto white background
            background.paste(resized, position, resized)
            
            # Save the icon
            output_path = os.path.join(output_dir, f'icon-{size}.png')
            background.save(output_path, 'PNG', optimize=True)
            print(f'Generated {size}x{size} icon: {output_path}')

def main():
    # Project root directory (one level up from scripts/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Source logo path (using logo2-removebg-preview.png as it already has transparency)
    source_logo = os.path.join(project_root, 'assets', 'logo2-removebg-preview.png')
    
    # Output directory for icons
    icons_dir = os.path.join(project_root, 'icons')
    
    # Generate icons
    generate_pwa_icons(source_logo, icons_dir)
    print('PWA icons generated successfully!')

if __name__ == '__main__':
    main()
