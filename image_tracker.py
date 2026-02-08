"""
Image tracker for managing the lifecycle of generated Bauhaus images.
Tracks when images were created and determines when they should be regenerated.
"""
import json
import os
from datetime import datetime, timedelta


TRACKER_FILE = 'assets/.image_tracker.json'


def load_tracker():
    """Load the image tracker data."""
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_tracker(data):
    """Save the image tracker data."""
    os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)
    with open(TRACKER_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def should_regenerate_images():
    """
    Check if images should be regenerated (after 2 days).
    Returns True if images should be regenerated, False otherwise.
    """
    tracker = load_tracker()
    
    if not tracker.get('last_generated'):
        return True
    
    last_generated = datetime.fromisoformat(tracker['last_generated'])
    time_since = datetime.now() - last_generated
    
    # Regenerate if it's been 2 days (48 hours)
    return time_since >= timedelta(days=2)


def get_time_remaining():
    """
    Get the time remaining until images should be regenerated.
    Returns a timedelta object or None if regeneration is due.
    """
    tracker = load_tracker()
    
    if not tracker.get('last_generated'):
        return timedelta(0)
    
    last_generated = datetime.fromisoformat(tracker['last_generated'])
    regenerate_time = last_generated + timedelta(days=2)
    remaining = regenerate_time - datetime.now()
    
    return remaining if remaining.total_seconds() > 0 else timedelta(0)


def update_tracker(image1_name, image2_name, theme1, theme2):
    """
    Update the tracker with new image generation information.
    
    Args:
        image1_name: Filename of the first generated image
        image2_name: Filename of the second generated image
        theme1: Theme of the first image ('balloon' or 'mnpluss')
        theme2: Theme of the second image ('balloon' or 'mnpluss')
    """
    tracker = {
        'last_generated': datetime.now().isoformat(),
        'images': [
            {'filename': image1_name, 'theme': theme1},
            {'filename': image2_name, 'theme': theme2}
        ]
    }
    save_tracker(tracker)


def get_current_images():
    """
    Get information about currently active images.
    Returns a list of dicts with 'filename' and 'theme', or empty list.
    """
    tracker = load_tracker()
    return tracker.get('images', [])


def cleanup_old_images():
    """
    Remove old images from the assets folder that are not the current pair.
    """
    tracker = load_tracker()
    current_images = {img['filename'] for img in tracker.get('images', [])}
    
    assets_folder = 'assets'
    if not os.path.exists(assets_folder):
        return
    
    for filename in os.listdir(assets_folder):
        filepath = os.path.join(assets_folder, filename)
        if (os.path.isfile(filepath) and 
            filename.endswith('.png') and 
            filename not in current_images and
            not filename.startswith('.')):  # Don't delete hidden files
            try:
                os.remove(filepath)
                print(f"Removed old image: {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")


if __name__ == '__main__':
    # Test the tracker
    print(f"Should regenerate: {should_regenerate_images()}")
    print(f"Time remaining: {get_time_remaining()}")
    print(f"Current images: {get_current_images()}")
