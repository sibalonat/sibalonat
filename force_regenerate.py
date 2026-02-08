#!/usr/bin/env python3
"""
Force regenerate images immediately (for testing).
This simulates what happens after 2 days have passed.
"""

import os
from bauhaus_generator import generate_image
from image_tracker import update_tracker, cleanup_old_images, get_current_images
from datetime import datetime
import random

print("🔄 Force Regenerating Images...")
print("=" * 60)

# Show current images
print("\n📸 Current images:")
for img in get_current_images():
    print(f"  - {img['filename']} (theme: {img['theme']})")

# Generate new images with different variations
themes = ['balloon', 'mnpluss']
theme1 = random.choice(themes)
theme2 = random.choice(themes)

# Use current timestamp for unique seeds
seed1 = int(datetime.now().timestamp())
seed2 = seed1 + 1

print(f"\n🎨 Generating new images:")
print(f"  Theme 1: {theme1} (seed: {seed1})")
print(f"  Theme 2: {theme2} (seed: {seed2})")

# Generate images
image1 = generate_image(theme1, width=1200, height=300, seed=seed1)
image2 = generate_image(theme2, width=1200, height=300, seed=seed2)

# Save with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
image1_name = f'{theme1}_{timestamp}_1.png'
image2_name = f'{theme2}_{timestamp}_2.png'

assets_folder = 'assets'
image1.save(os.path.join(assets_folder, image1_name))
image2.save(os.path.join(assets_folder, image2_name))

# Update tracker
update_tracker(image1_name, image2_name, theme1, theme2)

# Cleanup old images now that tracker is updated
print(f"\n🧹 Cleaning up old images...")
cleanup_old_images()

print(f"\n✅ Generated:")
print(f"  - {image1_name}")
print(f"  - {image2_name}")
print(f"\n⏰ These images will rotate in 2 days")
print("=" * 60)

# Show what's in assets now
print("\n📁 Current assets folder:")
for f in sorted(os.listdir(assets_folder)):
    if f.endswith('.png'):
        filepath = os.path.join(assets_folder, f)
        size = os.path.getsize(filepath) / 1024
        print(f"  ✓ {f} ({size:.1f} KB)")
