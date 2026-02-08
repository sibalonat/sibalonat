#!/usr/bin/env python3
"""
Test script to generate sample Bauhaus images without updating the README.
This allows you to preview the generated images before running the full update.
"""

from bauhaus_generator import generate_image
import os

# Create test output directory
test_dir = 'test_images'
os.makedirs(test_dir, exist_ok=True)

print("Generating test Bauhaus images...")
print("=" * 50)

# Generate balloon samples
print("\n🎈 Generating balloon theme samples...")
for i in range(3):
    seed = 100 + i
    img = generate_image('balloon', width=1200, height=300, seed=seed)
    filename = f'{test_dir}/balloon_sample_{i+1}.png'
    img.save(filename)
    print(f"  ✓ Saved: {filename}")

# Generate mnpluss samples
print("\n✨ Generating mnpluss theme samples...")
for i in range(3):
    seed = 200 + i
    img = generate_image('mnpluss', width=1200, height=300, seed=seed)
    filename = f'{test_dir}/mnpluss_sample_{i+1}.png'
    img.save(filename)
    print(f"  ✓ Saved: {filename}")

print("\n" + "=" * 50)
print(f"✅ Done! Generated 6 sample images in '{test_dir}/' directory")
print("\nYou can now preview these images to see the Bauhaus style.")
print("When ready, run 'python update_readme.py' to enable automatic")
print("image generation and README updates.")
