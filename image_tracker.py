"""
Image tracker for the Triadic Balloon hourly frame system.
Tracks the current frame and handles cleanup of old images.
"""

import json
import os
from datetime import datetime


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
    Check if a new frame should be generated.
    Returns True if the current hour differs from the last generated hour,
    or if no image has been generated yet.
    """
    tracker = load_tracker()

    if not tracker.get('last_generated'):
        return True

    current_hour = datetime.now().hour
    current_day = datetime.now().timetuple().tm_yday
    return (
        tracker.get('last_hour') != current_hour
        or tracker.get('day_seed') != current_day
    )


def get_time_remaining():
    """Return a human-readable string about the next frame change."""
    from datetime import timedelta
    now = datetime.now()
    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    remaining = next_hour - now
    minutes = int(remaining.total_seconds() // 60)
    return f"{minutes} minutes until next frame"


def update_tracker(filename, hour, day_seed):
    """
    Update the tracker with current frame information.

    Args:
        filename: Name of the generated image file
        hour:     Hour (0-23) of this frame
        day_seed: Day-of-year seed used for the cityscape
    """
    tracker = {
        'last_generated': datetime.now().isoformat(),
        'last_hour': hour,
        'day_seed': day_seed,
        'current_image': filename,
    }
    save_tracker(tracker)


def get_current_images():
    """
    Get information about the currently active image.
    Returns a list with one dict (for backward compat) or empty list.
    """
    tracker = load_tracker()
    if tracker.get('current_image'):
        return [{'filename': tracker['current_image'], 'theme': 'triadic'}]
    return []


def get_current_image():
    """Get the filename of the current image, or None."""
    tracker = load_tracker()
    return tracker.get('current_image')


def cleanup_old_images():
    """Remove old images from assets/ that are not the current frame."""
    tracker = load_tracker()
    current = tracker.get('current_image', '')

    assets_folder = 'assets'
    if not os.path.exists(assets_folder):
        return

    for filename in os.listdir(assets_folder):
        filepath = os.path.join(assets_folder, filename)
        if (os.path.isfile(filepath)
                and filename.endswith('.png')
                and filename != current
                and not filename.startswith('.')):
            try:
                os.remove(filepath)
                print(f"Removed old frame: {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")


if __name__ == '__main__':
    print(f"Should regenerate: {should_regenerate_images()}")
    print(f"Next change: {get_time_remaining()}")
    print(f"Current image: {get_current_image()}")
