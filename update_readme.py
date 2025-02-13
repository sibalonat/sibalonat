import os
import random

# Define the path to the assets folder and README.md file
assets_folder = 'assets'
readme_file = 'README.md'

# Get a list of all files in the assets folder
images = [f for f in os.listdir(assets_folder) if os.path.isfile(os.path.join(assets_folder, f))]

# Select a random image
random_image = random.choice(images)

# Read the current README.md content
with open(readme_file, 'r') as file:
    readme_content = file.readlines()

# Update the image URL in the README.md content
for i, line in enumerate(readme_content):
    if line.startswith('![Random Image]'):
        readme_content[i] = f'![Random Image]({assets_folder}/{random_image})\n'
        break

# Write the updated content back to README.md
with open(readme_file, 'w') as file:
    file.writelines(readme_content)