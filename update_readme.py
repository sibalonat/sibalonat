import os
import random
import requests
from datetime import datetime

# Define the path to the assets folder and README.md file
assets_folder = 'assets'
readme_file = 'README.md'
username = 'sibalonat'  # Replace with your GitHub username
token = os.getenv('GITHUB_TOKEN')  # Ensure you have set the GITHUB_TOKEN environment variable

# Get a list of all files in the assets folder
images = [f for f in os.listdir(assets_folder) if os.path.isfile(os.path.join(assets_folder, f))]

# Select a random image
random_image = random.choice(images)

# Fetch all repositories from GitHub API
headers = {'Authorization': f'token {token}'}
repos_url = "https://api.github.com/user/repos?visibility=all"
repos_response = requests.get(repos_url, headers=headers)

# Check if the request was successful
if repos_response.status_code != 200:
    raise Exception(f"Failed to fetch repositories: {repos_response.status_code} {repos_response.text}")

repos = repos_response.json()

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

# Update the image URL and recent activity in the README.md content
for i, line in enumerate(readme_content):
    if line.startswith('![Random Image]'):
        readme_content[i] = f'![Random Image]({assets_folder}/{random_image})\n'
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