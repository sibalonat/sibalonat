import os
import requests
from datetime import datetime
from bauhaus_generator import generate_triadic_frame, get_act
from image_tracker import (
    should_regenerate_images,
    update_tracker,
    get_current_image,
    cleanup_old_images,
    get_time_remaining,
)

# Define the path to the assets folder and README.md file
assets_folder = 'assets'
readme_file = 'README.md'
username = 'sibalonat'  # Replace with your GitHub username
token = os.getenv('GITHUB_TOKEN')  # Ensure you have set the GITHUB_TOKEN environment variable

# Ensure assets folder exists
os.makedirs(assets_folder, exist_ok=True)

# ── Generate the current Triadic Balloon frame ──────────────────────────────

now = datetime.now()
current_hour = now.hour
day_seed = now.timetuple().tm_yday

if should_regenerate_images():
    print(f"Generating Triadic Balloon frame for hour {current_hour} (act: {get_act(current_hour)})...")

    # Cleanup old frames first
    cleanup_old_images()

    # Generate the current frame
    img = generate_triadic_frame(hour=current_hour, day_seed=day_seed)

    # Save with descriptive name
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    image_name = f'triadic_{timestamp}_h{current_hour:02d}.png'
    img.save(os.path.join(assets_folder, image_name))

    # Update tracker
    update_tracker(image_name, current_hour, day_seed)

    print(f"Generated: {image_name}")
    print(f"Next frame: {get_time_remaining()}")
else:
    print(f"Current frame still valid for hour {current_hour}")
    current = get_current_image()
    if current:
        print(f"  Using: {current}")
    print(f"Next frame: {get_time_remaining()}")

# ── Select current image for README ─────────────────────────────────────────

current_image = get_current_image()
if not current_image:
    # Fallback: pick any PNG in assets
    images = [f for f in os.listdir(assets_folder)
              if f.endswith('.png') and not f.startswith('.')]
    current_image = images[0] if images else 'placeholder.png'

# ── Fetch GitHub stats ──────────────────────────────────────────────────────

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

# Calculate date 4 days ago from today
from datetime import timedelta
today = datetime.now()
four_days_ago = today - timedelta(days=4)

# Filter events from the last 4 days and aggregate by repo and date
activity_counter = {}
for event in events:
    if event['type'] in ['PushEvent', 'CreateEvent']:
        event_date_obj = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')

        # Skip if older than 4 days
        if event_date_obj < four_days_ago:
            continue

        repo_name = event['repo']['name']
        event_date = event_date_obj.strftime('%B %d, %Y')
        key = f"{repo_name}|{event_date}"

        if event['type'] == 'PushEvent':
            if key not in activity_counter:
                activity_counter[key] = {'type': 'Pushed to', 'count': 0, 'repo': repo_name, 'date': event_date}
            activity_counter[key]['count'] += 1
        else:
            # For CreateEvent, just add it once
            if key not in activity_counter:
                activity_counter[key] = {'type': 'Created', 'count': 1, 'repo': repo_name, 'date': event_date}

# Sort by count (most active first) and take top 4
sorted_activities = sorted(activity_counter.values(), key=lambda x: x['count'], reverse=True)[:4]

# Format the activity list
recent_activity = []
for activity in sorted_activities:
    if activity['type'] == 'Pushed to' and activity['count'] > 1:
        event_text = f"- {activity['type']} {activity['repo']} ({activity['count']} times) on {activity['date']}"
    elif activity['type'] == 'Pushed to':
        event_text = f"- {activity['type']} {activity['repo']} on {activity['date']}"
    else:
        event_text = f"- {activity['type']} {activity['repo']} on {activity['date']}"
    recent_activity.append(event_text)

# ── Update README.md ────────────────────────────────────────────────────────

with open(readme_file, 'r') as file:
    readme_content = file.readlines()

for i, line in enumerate(readme_content):
    if line.startswith('![Random Image]'):
        readme_content[i] = f'![Random Image]({assets_folder}/{current_image})\n'
    if line.startswith('🌟 **Public Repos:**'):
        readme_content[i] = f'🌟 **Public Repos:** {public_repos_count}\n'
    if line.startswith('🔒 **Private Repos:**'):
        readme_content[i] = f'🔒 **Private Repos:** {private_repos_count}\n'
    if line.startswith('## Recent Activity'):
        recent_activity_start = i + 1
        # Remove existing activity lines
        while recent_activity_start < len(readme_content) and readme_content[recent_activity_start].startswith('- '):
            readme_content.pop(recent_activity_start)
        # Also remove any blank lines after activity until we hit the next section
        while recent_activity_start < len(readme_content) and readme_content[recent_activity_start].strip() == '':
            readme_content.pop(recent_activity_start)
        # Insert new activity lines
        for activity in recent_activity:
            readme_content.insert(recent_activity_start, activity + '\n')
            recent_activity_start += 1
        break

# Write the updated content back to README.md
with open(readme_file, 'w') as file:
    file.writelines(readme_content)
