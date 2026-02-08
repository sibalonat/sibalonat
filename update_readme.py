import os
import random
import requests
from datetime import datetime
from bauhaus_generator import generate_image
from image_tracker import (
    should_regenerate_images, 
    update_tracker, 
    get_current_images,
    cleanup_old_images,
    get_time_remaining
)

# Define the path to the assets folder and README.md file
assets_folder = 'assets'
readme_file = 'README.md'
username = 'sibalonat'  # Replace with your GitHub username
token = os.getenv('GITHUB_TOKEN')  # Ensure you have set the GITHUB_TOKEN environment variable

# Ensure assets folder exists
os.makedirs(assets_folder, exist_ok=True)

# Check if we need to generate new images (every 2 days)
if should_regenerate_images():
    print("Generating new Bauhaus-style images...")
    
    # Cleanup old images first
    cleanup_old_images()
    
    # Randomly select two themes
    themes = ['balloon', 'mnpluss']
    theme1 = random.choice(themes)
    theme2 = random.choice(themes)
    
    # Generate unique seeds based on current time
    seed1 = int(datetime.now().timestamp())
    seed2 = seed1 + 1
    
    # Generate images
    image1 = generate_image(theme1, width=1200, height=300, seed=seed1)
    image2 = generate_image(theme2, width=1200, height=300, seed=seed2)
    
    # Save images with unique names based on timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    image1_name = f'{theme1}_{timestamp}_1.png'
    image2_name = f'{theme2}_{timestamp}_2.png'
    
    image1.save(os.path.join(assets_folder, image1_name))
    image2.save(os.path.join(assets_folder, image2_name))
    
    # Update tracker
    update_tracker(image1_name, image2_name, theme1, theme2)
    
    print(f"Generated: {image1_name} (theme: {theme1})")
    print(f"Generated: {image2_name} (theme: {theme2})")
    
    time_remaining = get_time_remaining()
    print(f"Next regeneration in: {time_remaining}")
else:
    print("Using existing images...")
    current_images = get_current_images()
    if current_images:
        for img in current_images:
            print(f"  - {img['filename']} (theme: {img['theme']})")
    time_remaining = get_time_remaining()
    print(f"Next regeneration in: {time_remaining}")

# Get a list of all PNG files in the assets folder (excluding hidden files)
images = [f for f in os.listdir(assets_folder) 
          if os.path.isfile(os.path.join(assets_folder, f)) 
          and f.endswith('.png') 
          and not f.startswith('.')]

# Select a random image from available images
if images:
    random_image = random.choice(images)
else:
    random_image = 'placeholder.png'  # Fallback

# Fetch all repositories from GitHub API (with pagination)
headers = {'Authorization': f'token {token}'}
repos = []
page = 1
per_page = 100

while True:
    repos_url = f"https://api.github.com/user/repos?visibility=all&per_page={per_page}&page={page}"
    repos_response = requests.get(repos_url, headers=headers)
    
    # Check if the request was successful
    if repos_response.status_code != 200:
        raise Exception(f"Failed to fetch repositories: {repos_response.status_code} {repos_response.text}")
    
    page_repos = repos_response.json()
    if not page_repos:
        break
    
    repos.extend(page_repos)
    page += 1

# Count public and private repositories
public_repos_count = sum(1 for repo in repos if not repo['private'])
private_repos_count = sum(1 for repo in repos if repo['private'])

# Fetch events for each repository
events = []
for repo in repos:
    events_url = f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/events"
    events_response = requests.get(events_url, headers=headers)
    
    # Check if the request was successful
    if events_response.status_code != 200:
        raise Exception(f"Failed to fetch events for {repo['name']}: {events_response.status_code} {events_response.text}")
    
    repo_events = events_response.json()
    events.extend(repo_events)

# Sort events by creation date in descending order
events.sort(key=lambda event: event['created_at'], reverse=True)

# Filter push and create events and count multiple pushes to the same project
recent_activity = []
event_counter = {}
for event in events:
    if event['type'] in ['PushEvent', 'CreateEvent']:
        repo_name = event['repo']['name']
        event_type = 'Pushed to' if event['type'] == 'PushEvent' else 'Created'
        event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%B %d, %Y')
        
        if event['type'] == 'PushEvent':
            if repo_name in event_counter:
                event_counter[repo_name] += 1
            else:
                event_counter[repo_name] = 1
            event_text = f'- {event_type} {repo_name} ({event_counter[repo_name]} times) on {event_date}'
        else:
            event_text = f'- {event_type} {repo_name} on {event_date}'
        
        if event['repo'].get('private'):
            event_text = event_text.replace(f'[{repo_name}](https://github.com/{repo_name})', repo_name)
        
        # Check if the event already exists in recent_activity
        existing_event = next((activity for activity in recent_activity if repo_name in activity and event_date in activity), None)
        if existing_event:
            recent_activity[recent_activity.index(existing_event)] = event_text
        else:
            recent_activity.append(event_text)
        
    if len(recent_activity) >= 20:
        break

# Read the current README.md content
with open(readme_file, 'r') as file:
    readme_content = file.readlines()

# Update the image URL, public and private repo counts, and recent activity in the README.md content
for i, line in enumerate(readme_content):
    if line.startswith('![Random Image]'):
        readme_content[i] = f'![Random Image]({assets_folder}/{random_image})\n'
    if line.startswith('🌟 **Public Repos:**'):
        readme_content[i] = f'🌟 **Public Repos:** {public_repos_count}\n'
    if line.startswith('🔒 **Private Repos:**'):
        readme_content[i] = f'🔒 **Private Repos:** {private_repos_count}\n'
    if line.startswith('## Recent Activity'):
        recent_activity_start = i + 1
        while readme_content[recent_activity_start].startswith('- '):
            readme_content.pop(recent_activity_start)
        for activity in recent_activity[:20]:  # Limit to 20 rows
            readme_content.insert(recent_activity_start, activity + '\n')
            recent_activity_start += 1
        break

# Write the updated content back to README.md
with open(readme_file, 'w') as file:
    file.writelines(readme_content)