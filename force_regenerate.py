#!/usr/bin/env python3
"""
Force regenerate the current Triadic Balloon frame (for testing).
Ignores the hourly check and generates the frame for the current hour.
"""

import os
from datetime import datetime
from bauhaus_generator import generate_triadic_frame, get_act
from image_tracker import update_tracker, cleanup_old_images, get_current_image

now = datetime.now()
current_hour = now.hour
day_seed = now.timetuple().tm_yday

print("Force Regenerating Triadic Balloon Frame...")
print("=" * 60)

# Show current image
current = get_current_image()
if current:
    print(f"\nCurrent image: {current}")

print(f"\nHour: {current_hour}  Act: {get_act(current_hour)}  Day seed: {day_seed}")

# Generate frame
img = generate_triadic_frame(hour=current_hour, day_seed=day_seed)

# Save
assets_folder = 'assets'
os.makedirs(assets_folder, exist_ok=True)
timestamp = now.strftime('%Y%m%d_%H%M%S')
image_name = f'triadic_{timestamp}_h{current_hour:02d}.png'
img.save(os.path.join(assets_folder, image_name))

# Update tracker and cleanup
update_tracker(image_name, current_hour, day_seed)
cleanup_old_images()

print(f"\nGenerated: {image_name}")

# Show what's in assets now
print(f"\nAssets folder:")
for f in sorted(os.listdir(assets_folder)):
    if f.endswith('.png'):
        filepath = os.path.join(assets_folder, f)
        size = os.path.getsize(filepath) / 1024
        print(f"  {f} ({size:.1f} KB)")

print("=" * 60)
