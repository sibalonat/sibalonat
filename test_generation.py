#!/usr/bin/env python3
"""
Test script: generates all 24 hourly frames of the Triadic Balloon journey.
Saves them to test_frames/ so you can preview the full daily cycle.
"""

import os
from bauhaus_generator import generate_triadic_frame, get_act

test_dir = 'test_frames'
os.makedirs(test_dir, exist_ok=True)

day_seed = 42  # fixed seed for consistent cityscape

print("Generating all 24 Triadic Balloon frames...")
print("=" * 55)

for hour in range(24):
    act = get_act(hour)
    img = generate_triadic_frame(hour=hour, day_seed=day_seed)
    filename = f'{test_dir}/frame_{hour:02d}_{act}.png'
    img.save(filename)
    print(f"  h{hour:02d}  act={act:6s}  -> {filename}")

print("=" * 55)
print(f"Done! 24 frames saved to '{test_dir}/'")
print("\nActs:  Yellow (0-7)  Red (8-15)  Blue (16-22)  Black (23)")
